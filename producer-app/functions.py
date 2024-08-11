from nats.aio.client import Client as NATS
import asyncio
import random
import string

async def produce_messages():
    # Connect to NATS
    nc = NATS()
    await nc.connect("nats://127.0.0.1:4222")  # Use the NATS service name as the hostname if running in Docker

    # Publish 50 random messages
    for _ in range(50):
        message = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        print(message)
        await nc.publish("producer-app-subject", message.encode())
        await asyncio.sleep(0.1)  # Simulate some delay between messages

    await nc.close()