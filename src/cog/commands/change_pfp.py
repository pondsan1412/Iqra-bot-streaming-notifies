from discord.ext import commands
from src.client.logic import change_profile
import discord.app_commands as app
import discord

class changepfp(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app.command()
    async def change_avatar(self, ctx: discord.Interaction, image_url: str):
        """
        Command to change the bot's profile picture using an image URL.
        Usage: /change_avatar <image_url>
        """
        # Check if the user is an administrator
        if not ctx.user.guild_permissions.administrator:
            await ctx.response.send_message(
                f"You do not have permission to use this command, {ctx.user.name}!" # Message visible only to the user
            )
            return

        # Attempt to change the bot's profile picture
        try:
            result = await change_profile.change_profile_picture(self.client, image_url)
            await ctx.response.send_message(result)
        except Exception as e:
            await ctx.response.send_message(f"Failed to change avatar: {str(e)}")

async def setup(client: commands.Bot):
    await client.add_cog(changepfp(client))
