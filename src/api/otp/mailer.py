import os
from dotenv import load_dotenv
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime, timedelta

load_dotenv()

class OTPMailer:
    def __init__(self, sender_email=None, sender_password=None):
        self.sender_email = sender_email or os.getenv("SENDER_EMAIL")
        self.sender_password = sender_password or os.getenv("SENDER_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.otp_store = {}  # เก็บ OTP ชั่วคราวใน dictionary (email -> {otp, timestamp})

    def generate_otp(self, length=6) -> str:
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=length))

    def send_otp_email(self, receiver_email: str) -> bool:
        """Generate and send OTP to the receiver's email, and store it"""
        otp = self.generate_otp()
        self.otp_store[receiver_email] = {
            "otp": otp,
            "timestamp": datetime.now()
        }

        subject = "Your One-Time Code"
        body = f"""
        Hello,

        Your one-time verification code is: {otp}
        This code will expire in 5 minutes.

        If you did not request this, please ignore this message.

        Regards,  
        Your Team
        """

        # Create email
        msg = MIMEMultipart()
        msg["From"] = f"Support <{self.sender_email}>"
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, msg.as_string())
            server.quit()
            logging.info(f"✅ OTP sent to {receiver_email} successfully")
            return True
        except Exception as e:
            logging.error(f"❌ Failed to send OTP: {e}")
            return False

    def verify_otp(self, email, user_otp):
        """Verify the OTP entered by the user."""
        if email not in self.otp_store:
            logging.warning(f"❌ No OTP found for '{email}'.")
            return False
        
        stored_otp_data = self.otp_store[email]
        stored_otp = stored_otp_data["otp"]
        otp_timestamp = stored_otp_data["timestamp"]

        # ตรวจสอบว่า OTP ตรงกันและยังไม่หมดอายุ (5 นาที)
        if stored_otp == user_otp and datetime.now() - otp_timestamp < timedelta(minutes=5):
            logging.info(f"✅ OTP for '{email}' verified successfully.")
            del self.otp_store[email]  # ลบ OTP ออกจาก dictionary หลังใช้งาน
            return True
        else:
            logging.warning(f"❌ OTP for '{email}' is invalid or expired.")
            return False

    def get_otp(self, email):
        """Get stored OTP for debugging (ใช้เฉพาะ log)."""
        return self.otp_store.get(email, {}).get("otp", None)
