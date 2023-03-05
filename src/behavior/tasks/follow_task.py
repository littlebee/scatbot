import asyncio

from commons import log


async def follow_task():
    while True:
        log.info("behavior follow task is running")
        await asyncio.sleep(30)
