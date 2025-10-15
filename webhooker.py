from flask import Flask, request
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, PushMessageRequest, TextMessage

CHANNEL_ACCESS_TOKEN = '5N9weT1wrJZK0InDEIw+yieWE+CT89KfwGHKarVkCBQ9Kd602FSPtS57rh5YZ4HxU66d9l9MsmRstoAEVs4SFBEBjWFR0+2fkQzXoSBlQPvK7rAtUF425p2wAMntUT0i7mKHaoqAhZ2R2QnTZvdVmQdB04t89/1O/w1cDnyilFU='
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
app = Flask(__name__)
serverlink = ""

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
                send_msg("your user_id:" + user_id, user_id)
        elif msg.get("text") == "SETTING":
            print("""
                    type: FIRST_TIME_SETTING to view your user id
                    type: LINK to get the server link
                  """
                  )
        elif msg.get("text") == "LINK":
            send_msg(serverlink, user_id)

        elif msg.get("text") == "HELP":
            web_link = ""
            send_msg(web_link, user_id)
        else:
            send_msg("Unknown command. Please type 'SETTING' for options.", user_id)

    return "OK", 200

def send_msg(texttosend, USER_ID):
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)

        message = TextMessage(text=texttosend)

        request = PushMessageRequest(
            to=USER_ID,
            messages=[message]
        )

        messaging_api.push_message(request)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
