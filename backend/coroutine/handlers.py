import asyncio
import time

from tornado.web import RequestHandler


class TimeConsumingHandler(RequestHandler):

    async def get(self):
        t1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        result = await self.do_task(5)
        t2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.write('Task start at:[{}], end at:[{}], return {} '.format(t1, t2, result))

    async def do_task(self, sec):
        await asyncio.sleep(sec)
        return 'done'
