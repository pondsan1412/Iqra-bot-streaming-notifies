import discord
from discord.ext import commands
import discord.app_commands as app
from src.client.logic import report_log
from src.client.logic import quarantine
from src.client.logic import requests

import asyncio

class lockdown_user(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client
    
    @app.command()
    async def verify(self, ctx:discord.Interaction, passkey:str):
        """to access this server you must input correct password"""
        await ctx.response.defer(thinking=True)
        try:
            #report
            await report_log.report_to_logCh(
                self.client,
                ctx.command.name,
                ctx.user.name,
                passkey
            )
            #check if password is correct
            p = await quarantine.fetch_passkey(self.client)
            if passkey != p:
                await ctx.followup.send("wrong password")
                return
            
            #user input correct password
            user_role = discord.utils.get(ctx.user.roles, name="Eskimo's")
            if user_role:
                await ctx.followup.send(f"you already have a role! {ctx.user.mention}")
            else:
                member = ctx.user
                add_this_role = discord.utils.get(ctx.guild.roles, name="Eskimo's")
                await member.add_roles(add_this_role)
                await ctx.followup.send(f"welcome to server! {member.mention}")
        except Exception as e:
            await ctx.followup.send(e)

    @app.command()
    async def register(self, ctx: discord.Interaction):
        # ตัวแปรสำหรับเก็บสถานะ
        role_accepted = None

        # สร้าง callback เพื่อรับผลลัพธ์จาก view
        def handle_accept(status: bool):
            nonlocal role_accepted
            role_accepted = status

        # ส่งคำขอไปยัง IQRA พร้อม callback
        await requests.request_to_accept_role(self.client, ctx, callback=handle_accept)
        await ctx.response.send_message("Command passed. Sending request to IQRA.")

        # รอผลลัพธ์จาก callback
        while role_accepted is None:
            await asyncio.sleep(1)

        # ตรวจสอบสถานะที่ได้รับ
        if role_accepted:
            await ctx.followup.send(
                content=f"You have been granted access to the server. "
                        f"Please read the rules and grab some roles. Enjoy! :) {ctx.user.mention}"
            )
        else:
            await ctx.followup.send(content="Your request has been refused.")



        

async def setup(client):
    await client.add_cog(lockdown_user(client))