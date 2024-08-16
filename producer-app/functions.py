from nats.aio.client import Client as NATS
import asyncio
import random
import string
from datetime import datetime
import json

async def produce_messages():
    # Connect to NATS
    nc = NATS()
    await nc.connect("nats://127.0.0.1:4222")  # Use the NATS service name as the hostname if running in Docker

    # Publish 50 random messages
    for _ in range(50):
        message_content = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        created_at = datetime.now().isoformat()

        message = {
            "content": message_content,
            "created_at": created_at
        }

        await nc.publish("producer-app-subject", json.dumps(message).encode())
        await asyncio.sleep(0.1)  # Simulate some delay between messages

    await nc.close()