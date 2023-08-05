import asyncio

from blockapi.block_observe import ObserveInfraredDistance
from blockapi.block_sound import PlayTTS
from dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, test_stop_run_program
from test.test_connect import test_get_device_by_name, test_start_run_program


async def test_ObserveInfraredDistance():
    observer: ObserveInfraredDistance = ObserveInfraredDistance()

    def handler(msg):
        print("{0}".format(str(msg.distance)))
        if msg.distance < 500:
            asyncio.create_task(__tts())

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts():
    await PlayTTS(text="是不是有人在啊， 你是谁啊").execute()


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveInfraredDistance())
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(test_stop_run_program())
        # asyncio.get_event_loop().run_until_complete(shutdown())
