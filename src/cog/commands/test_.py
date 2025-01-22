import discord
from discord.ext import commands
from src.client.logic import quarantine

class test_func(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.command()
    async def test_pull(self, ctx:commands.Context):
        l = quarantine
        pull_passkey = await l.fetch_passkey(client=self.client)
        await ctx.send(f"passkey is: {pull_passkey}")

async def setup(client):
    await client.add_cog(test_func(client))