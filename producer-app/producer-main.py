import asyncio
from flask import Flask, jsonify, request, render_template, redirect
from functions import *
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
# Produces random messages on a post request | should include some authentification mechanism
# @app.route("/trigger", methods=["POST"])
# def trigger_producer():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(produce_messages())
#     return jsonify({"status": "Messages produced"}), 200


# NATS publishing function
async def publish_to_nats(data):
    nc = NATS()
    await nc.connect(servers=["nats://nats:4222"])  # Replace with your NATS server
    await nc.publish("user-submission", json.dumps(data).encode())
    await nc.close()

# Webpage form that produces messages to Nats once submited
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/home")
def red_home():
    return redirect("/")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]

        data = {
            "name": name,
            "surname": surname,
            "email": email,
            "created_at": datetime.now().isoformat()
        }

        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(publish_to_nats(data))

    return render_template("submit.html", data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)