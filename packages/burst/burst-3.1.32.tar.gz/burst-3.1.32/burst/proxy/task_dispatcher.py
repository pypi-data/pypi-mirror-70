
from collections import defaultdict

from ..share import constants
from ..share.log import logger
from .group_queue import GroupQueue
from .reload_helper import ReloadHelper


class TaskDispatcher(object):
    """
    任务管理
    主要包括: 消息来了之后的分发
    """

    proxy = None

    # 之所以不用WeakSet的原因是，经过测试worker断掉之后，对象不会立即被删除，极有有可能会被用到。
    # 繁忙worker列表
    busy_workers_dict = None
    # 空闲
    idle_workers_dict = None
    # 消息队列
    group_queue = None

    # worker reload的帮助类
    reload_helper = None
    # reload结束后的回调
    reload_over_callback = None

    def __init__(self, proxy, reload_over_callback=None):
        self.busy_workers_dict = defaultdict(set)
        self.idle_workers_dict = defaultdict(set)

        self.proxy = proxy
        self.group_queue = GroupQueue(self.proxy.app.config['PROXY_MSG_QUEUE_MAX_SIZE'])
        self.reload_helper = ReloadHelper(self.proxy)
        self.reload_over_callback = reload_over_callback

    def remove_worker(self, worker):
        """
        删除worker，一般是worker断掉了
        :param worker:
        :return:
        """
        if worker in self.busy_workers_dict[worker.group_id]:
            self.busy_workers_dict[worker.group_id].remove(worker)

        elif worker in self.idle_workers_dict[worker.group_id]:
            self.idle_workers_dict[worker.group_id].remove(worker)

        # 这里的触发也是很神奇
        # 假设worker处理死循环了，在被监测到work超时之前，调用了burstctl reload
        # 就会出现新worker已经准备好了，但是老worker死了之后才会触发替换老worker
        if self.reload_helper.workers_done:
            self._try_replace_workers()

    def add_task(self, group_id, item):
        """
        添加任务
        当新消息来得时候，应该先检查有没有空闲的worker，如果没有的话，才放入消息队列
        :return:
        """
        if self.reload_helper.workers_done:
            # 不能丢消息
            if not self.group_queue.put(group_id, item):
                logger.error('put item fail. group_id: %s, queue_size: %s / %s',
                             group_id, self.group_queue.qsize(group_id), self.group_queue.max_size)

                self.proxy.stat_counter.add_discard_task(group_id)

            # 说明在reload，并且worker已经都ok了
            self._try_replace_workers()
            return

        idle_workers = self.idle_workers_dict[group_id]
        if not idle_workers:
            if not self.group_queue.put(group_id, item):
                logger.error('put item fail. group_id: %s, queue_size: %s / %s',
                             group_id, self.group_queue.qsize(group_id), self.group_queue.max_size)
                self.proxy.stat_counter.add_discard_task(group_id)
            return

        # 弹出一个可用的worker
        worker = idle_workers.pop()
        # 变成处理中
        worker.status = constants.WORKER_STATUS_BUSY
        # 放到队列中去
        self.busy_workers_dict[group_id].add(worker)

        # 让worker去处理任务吧
        worker.assign_task(item)

    def alloc_task(self, worker):
        """
        尝试获取新任务
        :return: 获取的新任务
        """
        if self.reload_helper.workers_done:
            # 说明在reload，并且worker已经都ok了
            worker.status = constants.WORKER_STATUS_IDLE
            # 同步状态
            self._sync_worker_status(worker)

            self._try_replace_workers()
            return None

        task = self.group_queue.get(worker.group_id)
        dst_status = constants.WORKER_STATUS_BUSY if task else constants.WORKER_STATUS_IDLE

        if worker.status != dst_status:
            # 说明状态有变化，需要调整队列
            worker.status = dst_status
            # 同步状态
            self._sync_worker_status(worker)

        return task

    def clear_tasks(self, group_id):
        """
        清空任务
        :param group_id:
        :return:
        """
        self.group_queue.clear(group_id)

    def clear_all_tasks(self):
        """
        清空所有任务
        :return:
        """
        self.group_queue.clear_all()

    def add_ready_worker(self, worker):
        # 设置为空闲状态
        worker.status = constants.WORKER_STATUS_IDLE
        self.reload_helper.add_worker(worker)

        if self.reload_helper.workers_done:
            self._try_replace_workers()

    def remove_ready_worker(self, worker):
        """
        删掉
        :param worker:
        :return:
        """
        self.reload_helper.remove_worker(worker)

    def start_reload(self):
        """
        开始reload
        :return:
        """
        self.reload_helper.start()

    def stop_reload(self):
        """
        停止reload
        :return:
        """
        self.reload_helper.stop()

    @property
    def reloading(self):
        return self.reload_helper.running

    def _try_replace_workers(self):
        """
        检查reload进度，如果已经全部切换完，尝试替换workers并分配任务
        :return:
        """

        for group_id, _workers in self.busy_workers_dict.items():
            if _workers:
                # 还有在运行中的workers
                return False

        # 到了这里，说明所有的workers都是空闲的了
        self.idle_workers_dict = dict(
            [(group_id, set() | _workers) for group_id, _workers in self.reload_helper.workers_dict.items()]
        )

        # 备份一份，马上要用
        bk_idle_workers_dict = dict(
            self.idle_workers_dict
        )

        # 一定要stop
        self.reload_helper.stop()

        # 分配现有的idle workers
        for group_id, _workers in bk_idle_workers_dict.items():
            for worker in _workers:
                if not worker.alloc_task():
                    # 一个group内的第一个分配不到task的worker，那么之后的也肯定分配不到了
                    break

        # 调用通知，workers已经替换完成
        self._on_workers_reload_over()
        return True

    def _sync_worker_status(self, worker):
        """
        内部 同步worker的状态：空闲/繁忙
        此时worker的status，已经自己改过了
        :param worker:
        :return:
        """

        if worker.status == constants.WORKER_STATUS_BUSY:
            src_workers_dict = self.idle_workers_dict
            dst_workers_dict = self.busy_workers_dict
        else:
            src_workers_dict = self.busy_workers_dict
            dst_workers_dict = self.idle_workers_dict

        if worker in src_workers_dict[worker.group_id]:
            # 因为有可能worker的状态是None的话，是不在任何队列里面的，所以先判断一下
            src_workers_dict[worker.group_id].remove(worker)

        dst_workers_dict[worker.group_id].add(worker)

    def _on_workers_reload_over(self):
        """
        当workers reload结束后的操作
        :return:
        """

        if self.reload_over_callback:
            self.reload_over_callback()
