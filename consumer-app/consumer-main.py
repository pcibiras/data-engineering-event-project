import asyncio
from nats.aio.client import Client as NATS
import mariadb
import logging
import os
import json
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')


async def run():
    nc = NATS()
    try:
        await nc.connect(servers=["nats://nats:4222"])
        logging.info("Connected to NATS server")
    except Exception as e:
        logging.error(f"Failed to connect to Nats: {e}")

    try:
        conn = mariadb.connect(
            user=mysql_user,
            password=mysql_password,
            host="mariadb_db",
            port=3306,
            database=mysql_database
        ) 
        cursor = conn.cursor()
        logging.info("Connection to db successful")

    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB Platform: {e}")


    async def message_handler(msg):

        subject = msg.subject
        message = msg.data.decode()
        logging.info(f"Received a message on '{subject}': {message}")
        msg_data = json.loads(message)
        name = msg_data["name"]
        surname = msg_data["surname"]
        email = msg_data["email"]
        created_at = msg_data["created_at"]

        try:
            cursor.execute(
                "INSERT INTO users (name, surname, email, created_at) VALUES (?, ?, ?, ?)",
                (name, surname, email, created_at)
            )
            conn.commit()
        except mariadb.Error as e:
            print(f"Failed to save message to database: {e}")

    await nc.subscribe("user-submission", cb=message_handler)

    await asyncio.Event().wait()

if __name__ == "__main__":
    logging.info("Starting consumer app")
    logging.info("Waiting for the db container")
    time.sleep(30)
    asyncio.run(run())