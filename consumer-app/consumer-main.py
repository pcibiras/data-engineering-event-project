import asyncio
from nats.aio.client import Client as NATS
import mariadb
import os

mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')

async def run():
    nc = NATS()
    await nc.connect(servers=["nats://nats:4222"])

    conn = mariadb.connect(
        user=mysql_user,
        password=mysql_password,
        host="127.0.0.1",
        port="3306",
        database=mysql_database
    ) 
    cursor = conn.cursor()

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")

        cursor.execute("INSERT INTO messages (content) VALUES (?)", (data,))
        conn.commit()

    await nc.subscribe("producer-app-subject", cb=message_handler)

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run())