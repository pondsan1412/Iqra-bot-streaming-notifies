# src/cog/commands/register_db.py

import discord
from discord.ext import commands
from src.api import iicemkdatabase
from src.api.otp.mailer import OTPMailer
import os
from dotenv import load_dotenv
import discord.app_commands as app_commands
import asyncio
import logging
import re
load_dotenv()

class PhpMyAdmin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.otp_store = {}  # Store OTPs temporarily for verification
        self.mailer = None # OTPMailer instance
        email = os.getenv("SENDER_EMAIL")
        password = os.getenv("SENDER_PASSWORD")

        try:
            self.mailer = OTPMailer(sender_email=email, sender_password=password)
            logging.info("✅ OTPMailer initialized successfully.")
        except Exception as e:
            logging.error(f"❌ Error initializing OTPMailer: {e}")
            raise e

    @app_commands.command()
    async def register_to_access_database(self, interaction: discord.Interaction):
        """ลงทะเบียน MySQL User สำหรับ Read-Only Access"""
        await interaction.response.defer(thinking=True)

        # ✅ Step 1: ถามอีเมล
        while True:
            await interaction.followup.send("📩 Please enter your email address:")

            def check_email(message):
                return message.author == interaction.user and message.channel == interaction.channel

            try:
                email_msg = await self.client.wait_for("message", timeout=300.0, check=check_email)
                email = email_msg.content.strip()
            except asyncio.TimeoutError:
                await interaction.followup.send("⏳ You took too long to respond. Please try again.")
                continue  

            # ✅ ตรวจสอบว่าอีเมลซ้ำหรือไม่
            email_exists = iicemkdatabase.check_email_exists(email)

            if email_exists:
                await interaction.followup.send(f"❌ Email `{email}` is already registered. Please enter a different email.")
                continue  
            else:
                break  

        # ✅ Step 2: ถาม Username
        while True:
            await interaction.followup.send("👤 Please enter the username you want to use (max 12 characters, no special symbols):")

            def check_username(message):
                return message.author == interaction.user and message.channel == interaction.channel

            try:
                username_msg = await self.client.wait_for("message", timeout=300.0, check=check_username)
                username = username_msg.content.strip()
            except asyncio.TimeoutError:
                await interaction.followup.send("⏳ You took too long to respond. Please try again.")
                continue  

            # ✅ ตรวจสอบ username
            if len(username) > 12:
                await interaction.followup.send("❌ Username cannot exceed 12 characters. Please enter a shorter username.")
                continue  
            if not re.match(r"^[a-zA-Z0-9_]+$", username):
                await interaction.followup.send("❌ Username cannot contain special characters. Only letters, numbers, and underscores (_) are allowed.")
                continue  

            break  

        # ✅ Step 3: ถาม Password
        while True:
            await interaction.followup.send("🔒 Please enter a password (at least 6 characters):")

            def check_password(message):
                return message.author == interaction.user and message.channel == interaction.channel

            try:
                password_msg = await self.client.wait_for("message", timeout=60.0, check=check_password)
                password = password_msg.content.strip()
            except asyncio.TimeoutError:
                await interaction.followup.send("⏳ You took too long to respond. Please try again.")
                continue  

            if len(password) < 6:
                await interaction.followup.send("❌ Password too short. Please enter at least 6 characters.")
                continue  
            else:
                break  

        # ✅ Step 4: ส่ง OTP
        otp_sent = self.mailer.send_otp_email(email)

        if not otp_sent:
            await interaction.followup.send("❌ Failed to send OTP. Please try again later.")
            return

        await interaction.followup.send("📧 An OTP has been sent to your email. Please reply with the OTP to complete registration:")

        # ✅ Step 5: ตรวจสอบ OTP
        while True:
            def check_otp(message):
                return message.author == interaction.user and message.channel == interaction.channel

            try:
                otp_msg = await self.client.wait_for("message", timeout=300.0, check=check_otp)
                user_otp = otp_msg.content.strip()
            except asyncio.TimeoutError:
                await interaction.followup.send("⏳ OTP verification timed out. Please enter the OTP again.")
                continue  

            stored_otp = self.mailer.get_otp(email)

            if stored_otp is None:
                await interaction.followup.send("❌ OTP expired or not found. Please try again.")
                continue  

            if stored_otp != user_otp:
                await interaction.followup.send("❌ Invalid OTP. Please ensure you've entered the correct code.")
                continue  
            else:
                break  

        # ✅ Step 6: ลงทะเบียน MySQL User
        success = iicemkdatabase.create_readonly_user(email, username, password)

        if success:
            await interaction.followup.send(
                f"✅ **Registration successful!** 🎉\n"
                f"**Username:** `{username}`\n"
                f"**Password:** `{password}`\n"
                f"📌 You can now log in to phpMyAdmin at: [Database](http://iicemk.ddns.net/)"
            )
        else:
            await interaction.followup.send("❌ Registration failed. Please try again.")


async def setup(client):
    await client.add_cog(PhpMyAdmin(client))
