import discord
from discord.ext import commands
from src.client.logic import quarantine

class test_func(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.command()
    async def check_role(self, ctx:commands.Context):
        role = discord.utils.get(
            ctx.author.roles,
            name="Eskimo's"
        )
        if role:
            await ctx.reply(f" role is true: {role.name}")
        else:
            await ctx.reply(f"None")
        

async def setup(client):
    await client.add_cog(test_func(client))