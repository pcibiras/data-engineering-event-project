import asyncio
from flask import Flask, jsonify
from functions import produce_messages

async def run_producer():
    await produce_messages()

if __name__ == "__main__":
    asyncio.run(run_producer())