import asyncio
import itertools


async def spin(msg):
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        print(status, flush=True, end='\r')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError: # 取消Task对象会抛出异常
            break
    print(' ' * len(status), end='\r')
    
    
async def slow_function():
    await asyncio.sleep(3)
    return 42



async def supervisor():
    spinner = asyncio.create_task(spin('thinking!'))
    print('spinner object:', spinner)
    result = await slow_function()
    spinner.cancel() # 取消Task对象
    return result


def main():
    result = asyncio.run(supervisor())
    print('Answer:', result)
    
    
if __name__ == '__main__':
    main()