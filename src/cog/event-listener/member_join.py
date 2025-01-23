import discord
from discord.ext import commands
from src.client.logic import report_log

class event_member(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        
        role = discord.utils.get(member.guild.roles, name="blinded")
        
        await member.add_roles(role)
        
            
async def setup(client):
    await client.add_cog(event_member(client))