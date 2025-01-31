import discord
from discord.ext import commands
from src.automate import fun_count

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

        #//counting number of messages in the channel and rickrool the user if the number is the same as the random number between 1-10 every 5 messages
        count_instance = fun_count.Count(0)
        await count_instance.counting(message)
        
                    
                    
async def setup(client):
    await client.add_cog(ignoreMessage(client))