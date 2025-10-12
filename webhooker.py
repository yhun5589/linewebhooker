from flask import Flask, request
from message_sender_line import send_msg
import os

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    data = request.get_json()
    print("Webhook received:", data)

    for event in data.get("events", []):
        if event.get("type") != "message":
            continue

        msg = event.get("message", {})
        if msg.get("type") != "text":
            continue

        if msg.get("text") == "FIRST_TIME_SETTING":
            user_id = event.get("source", {}).get("userId")
            if user_id:
                send_msg(user_id)

    return "OK", 200


# Optional test route to prevent 404 on root
@app.route("/", methods=['GET'])
def home():
    return "Bot is running!", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
