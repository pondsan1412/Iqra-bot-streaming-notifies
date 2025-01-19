from discord.ext import commands
from src.client.logic import change_profile
import discord.app_commands as app
import discord

class changepfp(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @app.command()
    async def change_avatar(self, ctx: discord.Interaction, image_url: str):
        """
        Command to change the bot's profile picture using an image URL.
        Usage: !changeavatar <image_url>
        """
        if not ctx.user.guild_permissions.administrator:
            await ctx.response.send_message(
                f"You do not have permission to use this command! {ctx.user.name}"
            )
        result = await change_profile.change_profile_picture(self.client, image_url)
        await ctx.response.send_message(result)
        
async def setup(client: commands.Bot):
    await client.add_cog(changepfp(client))