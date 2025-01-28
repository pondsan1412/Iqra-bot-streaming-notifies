import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.api import iicemkdatabase as Database
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OTPMailer:
    def __init__(self, sender_email=None, sender_password=None):
        self.sender_email = sender_email or os.getenv("SENDER_EMAIL")
        self.sender_password = sender_password or os.getenv("SENDER_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.db = Database()  # เชื่อมกับฐานข้อมูล

    def generate_otp(self, length=6) -> str:
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=length))

    def send_otp_email(self, receiver_email: str) -> bool:
        """Generate and send OTP to the receiver's email"""
        otp = self.generate_otp()
        self.db.save_otp(receiver_email, otp)  # Save OTP to the database

        subject = "Your One-Time Code"
        body = f"""
        Hello,

        Your one-time verification code is: {otp}
        This code will expire in 5 minutes.

        If you did not request this, please ignore this message.

        Regards,  
        iicemk Team
        """

        # Create email
        msg = MIMEMultipart()
        msg["From"] = f"iicemk Support <{self.sender_email}>"
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            # Connect to Gmail's SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, msg.as_string())
            server.quit()
            logger.info(f"✅ OTP sent to {receiver_email} successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send OTP: {e}")
            return False

    def verify_otp(self, email: str, user_otp: str) -> bool:
        """Verify the OTP"""
        return self.db.verify_otp(email, user_otp)
