import asyncio

from blockapi.block_content import QueryWiKi, StartTranslate
from dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name


async def test_query_wiki():
    block: QueryWiKi = QueryWiKi(query='优必选')
    response = await block.execute()
    print(f'test_query_wiki: {response}')


async def test_start_translate():
    block: StartTranslate = StartTranslate(query="张学友")
    response = await block.execute()
    print(f'test_start_translate: {response}')


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_query_wiki())
        asyncio.get_event_loop().run_until_complete(test_start_translate())
        asyncio.get_event_loop().run_until_complete(shutdown())
