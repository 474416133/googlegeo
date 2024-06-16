#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：babikill -> starters
@IDE    ：PyCharm
@Author ：sven
@Date   ：2024/6/16 10:43
@Desc   ：
"""
import asyncio
import logging
import pika
from biubiu.application import URL


logger = logging.getLogger('biubiu.starters')


class PikaConsumerStarter:
    """
    简单的实现了一个 支持消费RabbitMQ消息的Starter, 实现一个Starter需要实现loop方法
    例如：
    class Starter:

        async def loop():
            #
            pass
    """
    QUEUE = 'googlegeo'


    def __init__(self, amqp_url, app):
        self._conn = pika.BlockingConnection(parameters=pika.URLParameters(amqp_url))
        self.channel = self._conn.channel()
        self.channel.basic_consume(self.QUEUE, self.on_message, auto_ack=True)
        self.app = app


    def on_message(self, _unused_channel, basic_deliver, properties, body):
        print('body: {}'.format(body.decode('utf-8')))
        self.app.put(URL(body.decode('utf-8')))


    async def loop(self):
        await asyncio.get_event_loop().run_in_executor(None, self.run)


    def close(self):
        self._conn.close()


    def run(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

if __name__ == '__main__':
    pika_starter = PikaConsumerStarter('amqp://guest:guest@localhost:5672/%2F', None)
    pika_starter.run()