#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：babikill -> application
@IDE    ：PyCharm
@Author ：sven
@Date   ：2024/6/15 20:09
@Desc   ：
"""
import sys
import inspect
import functools
import logging
import asyncio
import contextlib
from asyncio.queues import LifoQueue


logger = logging.getLogger('biubiu')


class ErrorStack:
    """
    主要用于异常处理
    """
    def __init__(self, exception, msg, tb):
        self.exception = exception
        self.tb = tb



class Application:

    def __init__(self, worker_id, starters=None, scope_context_manager=None):
        """
        :param worker_id:
        :param starters: 主要是实现 从 第三方消息中间件获取任务, 并把任务放进队列中，整个应用流程如下：
                                task
         redis/rabbitMQ/kaffa/  ===>    application._queue  ===>  handler(app, task)
                                          返回结果重新放进队列  <==
        :param scope_context: scope 上下文管理器，主要用于应用启动前及关闭前做的一些工作，比如初始化数据库连接等
        一般定义如下
        async def _scope(app):
            #
            await conn()
            app.db = conn
            yield
            del app.dp
            conn.close()

        """
        self.worker_id = worker_id
        self._queue = LifoQueue()
        self._starters = starters or []
        self._scope_context_manager = contextlib.asynccontextmanager(scope_context_manager or self._default_scope_context_manager)
        self._handlers = {}


    def add_starter(self, starter):
        """
        star
        :param starter:
        :return:
        """
        self._starters.append(starter)


    def add_handler(self, match_cls, handler):
        """
        :param match_cls:
        :param handler: 处理器，callable， 参数(application, task)
        :return:
        """
        if match_cls in self._handlers:
            logger.warning("{}'s handler had set, ignore this set".format(match_cls))
        else:
            self._handlers[match_cls] = handler


    def handle(self, match_cls):
        def _wrap(handler):
            self.add_handler(match_cls, handler)
        return _wrap


    async def _loop(self):
        async with self._scope_context_manager(self):
            while 1:
                task = await self._queue.get()
                self._queue.task_done()
                await self(task)


    async def _start(self):
        tasks = [starter(self) for starter in self._starters]
        tasks.insert(0, self._loop())
        await asyncio.gather(*tasks)


    def run(self, url=None):
        self._queue.put_nowait(url)
        asyncio.run(self._start())


    async def _default_scope_context_manager(self, app):
        """这是默认的scop管理器
        """

        yield


    async def __call__(self, task):
        async def _handle_ret(ret):
            if ret and self._match(ret):
                await self._queue.put(ret)

        handler = self._match(task)
        if not handler:
            logger.warning('no such handler handle {}, task : {}'.format(task.__class__, task))
        else:
            try:
                if not asyncio.iscoroutinefunction(handler) and not inspect.isasyncgenfunction(handler):
                    ret = await asyncio.get_event_loop().run_in_executor(None, handler, self, task)
                    await _handle_ret(ret)
                elif inspect.isasyncgenfunction(handler):
                    async for item in handler(self, task):
                        await _handle_ret(item)
                else:
                    ret = await handler(self, task)
                    await _handle_ret(ret)
            except:
                logger.exception('error occur when handle task {}. '.format(task))
                ret = ErrorStack(*sys.exc_info())
                await _handle_ret(ret)



    def _match(self, task):
        """
        根据task 匹配对应的处理器
        :param task:
        :return:
        """
        handler = self._handlers.get(task.__class__)
        if not handler:
            for key in self._handlers:
                if isinstance(task, key):
                    handler = self._handlers[key]
                    break
        return handler

