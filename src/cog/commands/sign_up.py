import discord
from discord.ext import commands
import discord.app_commands as app
from src.client.logic import sign_up
from src.client.views import signup_view

class signup(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @app.command()
    async def sign_up(self, ctx:discord.Interaction):
        await ctx.response.defer(thinking=True)
        call_view = signup_view.signup_button_viewer()
        await ctx.followup.send(view=call_view, content="people sign up by vote")
        

async def setup(client):
    await client.add_cog(signup(client))