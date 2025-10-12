from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, PushMessageRequest, TextMessage

# Replace this with your real Channel Access Token
CHANNEL_ACCESS_TOKEN = '5N9weT1wrJZK0InDEIw+yieWE+CT89KfwGHKarVkCBQ9Kd602FSPtS57rh5YZ4HxU66d9l9MsmRstoAEVs4SFBEBjWFR0+2fkQzXoSBlQPvK7rAtUF425p2wAMntUT0i7mKHaoqAhZ2R2QnTZvdVmQdB04t89/1O/w1cDnyilFU='
USER_ID = 'U62861b537edda7b2bee65f9db1620aa5'
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

# Replace with the user's LINE ID or your own ID for testing
def send_msg(texttosend):
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)

        message = TextMessage(text=texttosend)

        request = PushMessageRequest(
            to=USER_ID,
            messages=[message]
        )

        messaging_api.push_message(request)

if __name__ == "__main__":
    send_msg("⚠️ now it starts")