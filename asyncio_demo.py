import asyncio
import time
from asyncio import TaskGroup, Task

l = []

async def wait(sec):
    print(f"I'm going to wait for {sec} secs")
    l.append(sec)
    pre_len = len(l)
    await asyncio.sleep(sec)
    if pre_len == 1:
        print('only one')

    print(f"Finished waiting {sec} secs")

async def main():
    s = time.time()
    print('hello')
    # await asyncio.sleep(2)
    # await asyncio.sleep(1)
    # task1 = asyncio.create_task(wait(2))
    # task2 = asyncio.create_task(wait(1))

    # await task1
    # await task2

    # await asyncio.gather(task1, task2)

    tasks: list[Task] = []
    async with TaskGroup() as tg:
        for i in range(5, 0, -1):
            tasks.append(tg.create_task(wait(i)))
    print(time.time()-s, 'bye')

    # tasks[0].add_done_callback()
asyncio.run(main())

