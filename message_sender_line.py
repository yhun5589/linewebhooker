import cv2
import requests
from io import BytesIO
from PIL import Image
import os
from linebot.v3.messaging import (
    MessagingApi,
    Configuration,
    ApiClient,
    PushMessageRequest,
    ImageMessage,
    TextMessage
)

# LINE credentials
CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
USER_ID = os.environ.get("USER_ID")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

# --- Send text message ---
def send_msg(texttosend):
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        message = TextMessage(text=texttosend)
        request = PushMessageRequest(to=USER_ID, messages=[message])
        messaging_api.push_message(request)

# --- Upload image ---
def upload_image(frame):
    # Convert OpenCV frame to JPEG bytes
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(frame_rgb)
    img_byte_arr = BytesIO()
    img_pil.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # === Try 0x0.st first ===
    try:
        files = {'file': ('frame.jpg', img_byte_arr, 'image/jpeg')}
        response = requests.post('https://0x0.st', files=files, headers=headers, timeout=10)
        if response.status_code == 200 and "http" in response.text:
            link = response.text.strip()
            print("✅ Uploaded to 0x0.st:", link)
            return link
        else:
            print("❌ 0x0.st upload failed:", response.status_code, response.text)
    except Exception as e:
        print("❌ 0x0.st exception:", e)

    # === Fallback to catbox.moe === (rarely blocked, very reliable)
    try:
        img_byte_arr.seek(0)
        files = {'fileToUpload': ('frame.jpg', img_byte_arr, 'image/jpeg')}
        response = requests.post('https://catbox.moe/user/api.php', data={'reqtype': 'fileupload'}, files=files, headers=headers, timeout=15)
        if response.status_code == 200 and "http" in response.text:
            link = response.text.strip()
            print("✅ Uploaded to Catbox:", link)
            return link
        else:
            print("❌ Catbox upload failed:", response.status_code, response.text)
    except Exception as e:
        print("❌ Catbox exception:", e)

    return None


# --- Send frame as LINE image message ---
def send_opencv_frame(frame):
    img_url = upload_image(frame)
    if not img_url:
        print("❌ Upload failed completely")
        send_msg("⚠️ Image upload failed")
        return

    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        message = ImageMessage(original_content_url=img_url, preview_image_url=img_url)
        request = PushMessageRequest(to=USER_ID, messages=[message])
        messaging_api.push_message(request)

    print("✅ Frame sent to LINE:", img_url)


# --- Test ---
if __name__ == "__main__":
    frame = cv2.imread("hq720.jpg")  # Replace with your test image
    send_msg("⚠️ Sending test image...")
    send_opencv_frame(frame)

