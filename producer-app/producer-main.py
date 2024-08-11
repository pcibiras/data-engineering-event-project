import asyncio
from flask import Flask, jsonify
from functions import *

app = Flask(__name__)

@app.route("/trigger", methods=["POST"])
def trigger_producer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(produce_messages())
    return jsonify({"status": "Messages produced"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)