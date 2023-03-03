import asyncio


async def follow_task():
    while True:
        print("behavior follow task is running")
        asyncio.sleep(1)
