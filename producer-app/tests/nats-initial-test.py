import asyncio
from nats.aio.client import Client as NATS

async def run_test():
    nc = NATS()
    
    async def message_handler(msg):
        print(f"Received a message: {msg.data.decode()}")
        await nc.close()

    await nc.connect("nats://127.0.0.1:4222")
    await nc.subscribe("test", cb=message_handler)
    await nc.publish("test", b"Hello from NATS!")
    await asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_test())