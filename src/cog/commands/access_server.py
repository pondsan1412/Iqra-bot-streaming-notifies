import discord
from discord.ext import commands
import discord.app_commands as app
from src.client.logic import report_log
from src.client.logic import quarantine

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
            
            await ctx.followup.send("code passed!")
        except Exception as e:
            await ctx.followup.send(e)

async def setup(client):
    await client.add_cog(lockdown_user(client))