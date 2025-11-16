from flask import Flask, request, jsonify
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, PushMessageRequest, TextMessage
import os

CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
app = Flask(__name__)
serverlink = ""

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
messaging_api = MessagingApi(ApiClient(configuration))

# Helper function to send messages
def send_msg(user_id, text):
    try:
        request_body = PushMessageRequest(
            to=user_id,
            messages=[TextMessage(text=text)]
        )
        messaging_api.push_message(request_body)
    except Exception as e:
        print(f"Error sending message: {e}")

# Main webhook endpoint
@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()
    events = body.get("events", [])

    for event in events:
        # Only handle messages from users
        if event.get("type") != "message":
            continue

        source = event.get("source", {})
        user_id = source.get("userId")
        if not user_id:
            # Skip events without userId
            print("No userId found in event, skipping.")
            continue

        message = event.get("message", {})
        message_type = message.get("type")
        text = message.get("text", "").strip().upper()

        # Handle only text messages
        if message_type != "text":
            continue

        # Decide what to respond
        if text == "HELP":
            send_msg(user_id, "Here is the help info you need.")
        elif text == "SETTING":
            send_msg(user_id, "Type FIRST_TIME_SETTING to view your user id or LINK to get setup procedure link.")
        elif text == "FIRST_TIME_SETTING":
            send_msg(user_id, f"Your user ID is: {user_id}")
        elif text == "LINK":
            send_msg(user_id, "for setup procedures check https://www.instagram.com/tu_robotclub/")
        else:
            send_msg(user_id, f"You said: {text}")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



