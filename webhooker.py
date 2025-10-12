from flask import Flask, request
import json
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage
)

# ---------------- Config ----------------
CHANNEL_ACCESS_TOKEN = "5N9weT1wrJZK0InDEIw+yieWE+CT89KfwGHKarVkCBQ9Kd602FSPtS57rh5YZ4HxU66d9l9MsmRstoAEVs4SFBEBjWFR0+2fkQzXoSBlQPvK7rAtUF425p2wAMntUT0i7mKHaoqAhZ2R2QnTZvdVmQdB04t89/1O/w1cDnyilFU="
DATA_FILE = "user_ids.json"  # where userIds will be saved

# LINE API setup
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
app = Flask(__name__)

# Load existing userIds or start fresh
try:
    with open(DATA_FILE, "r") as f:
        user_ids = set(json.load(f))
except FileNotFoundError:
    user_ids = set()


# ---------------- Webhook ----------------
@app.route("/callback", methods=['POST'])
def callback():
    data = request.get_json()
    
    for event in data.get("events", []):
        source = event.get("source", {})
        if source.get("type") == "user":
            user_id = source.get("userId")
            if user_id not in user_ids:
                user_ids.add(user_id)
                print(f"New userId collected: {user_id}")
                # Save updated list
                with open(DATA_FILE, "w") as f:
                    json.dump(list(user_ids), f)
    
    return "OK", 200


# ---------------- Send Message to All Users ----------------
@app.route("/send_message", methods=['POST'])
def send_message():
    message_text = request.json.get("text", "Hello from your bot!")
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        for uid in user_ids:
            request_body = PushMessageRequest(
                to=uid,
                messages=[TextMessage(text=message_text)]
            )
            try:
                messaging_api.push_message(push_message_request=request_body)
                print(f"Message sent to {uid}")
            except Exception as e:
                print(f"Failed to send to {uid}: {e}")
    return "Messages sent", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
