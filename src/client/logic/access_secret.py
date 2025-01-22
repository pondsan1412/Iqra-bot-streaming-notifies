from dotenv import load_dotenv
import os
import datetime
from pytz import timezone

class secret_chest():
    def __init__(self):
        self.key = os.getenv(key="SECRET_PASSKEY")
        self.locker = True
        self.file = os.getenv(key="RONALD_FACE_REVEAL")
        self.fixTime = os.getenv(key="FIX_TIME")

    def checktime(self):
        """
        Check if time is between midnight and 9:00 AM in Thailand.
        If time is in the restricted range, return False to stop execution.
        """
        thailand_tz = timezone('Asia/Bangkok')  # กำหนด timezone เป็นกรุงเทพฯ
        current_time = datetime.datetime.now(thailand_tz)  # ใช้เวลาปัจจุบันของกรุงเทพฯ
        current_hrs = current_time.hour  # ดึงชั่วโมงจากเวลาปัจจุบัน

        # ตรวจสอบว่าอยู่ในช่วงเวลา 00:00 ถึง 09:00 หรือไม่
        if 0 <= current_hrs < 9:
            print(f"Access denied. Current time: {current_time}")  # แสดงเวลาปัจจุบัน
            return False  # หากในช่วงเวลาห้ามให้หยุดการทำงาน

        print(f"Access granted. Current time: {current_time}")  # แสดงเวลาปัจจุบัน
        return True
    
    async def antiTrollUser(self, ctx, userBorndate: str):
        """
        check if user using their ult account so function will refuse to continue
        userBorndate: must be ctx.created_at or something
        """
        member = ctx.author
        created_at = member.created_at
        try:
            user_born = datetime.datetime.strptime(userBorndate, '%Y-%m-%d')
        except ValueError:
            await ctx.send("Invalid date format. Please use 'YYYY-MM-DD.' ")
            return
        if created_at.date() > user_born.date():
            await ctx.send("It seems like you're using an alt account. Action is blocked.")
        else:
            await ctx.send("Account verified. You are good to go!")
            

        