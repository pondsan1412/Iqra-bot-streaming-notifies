from src.api import twitch_api
from dotenv import load_dotenv
import os
import json

# โหลด environment variables
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID_TW")
CLIENT_SECRET = os.getenv("CLIENT_SECRET_TW")

# สร้างอินสแตนซ์ของ API
api = twitch_api.TwitchAPI(CLIENT_ID, CLIENT_SECRET)

# เรียกข้อมูลผู้ใช้
username = "aceu"
user_data = api.get_user(username)
if user_data:
    user_id = user_data[0]["id"]
    print("User Data:", json.dumps(user_data, indent=4))

    # ตรวจสอบสถานะ Live
    try:
        live_status = api.check_live_status(user_id)
        print("Live Status:", json.dumps(live_status, indent=4))
    except Exception as e:
        print(f"Error checking live status: {e}")

    # ดึงข้อมูลคลิป
    try:
        clips_data = api.get_clips(user_id)
        print("Clips Data:", json.dumps(clips_data, indent=4))
    except Exception as e:
        print(f"Error fetching clips: {e}")

else:
    print("User not found!")
