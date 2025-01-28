import discord
from discord.ext import commands


class ignoreMessage(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        """ignore self message to avoid spamming hell"""
        if message.author == self.client.user:
            return
        # if message.author.id == 324207503816654859:
        #     await quarantine.is_online_courantine(message)
        
async def setup(client):
    await client.add_cog(ignoreMessage(client))