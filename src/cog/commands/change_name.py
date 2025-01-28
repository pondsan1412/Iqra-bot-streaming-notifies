import discord
from discord.ext import commands
from discord import app_commands

class change_name_(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command()
    async def change_name(self, ctx: discord.Interaction, what_name:str):
        """ change bot name"""
        await ctx.response.defer(thinking=True)
        if not ctx.user.guild_permissions.administrator:
            await ctx.response.send_message(
                f"You do not have permission to use this command! {ctx.user.name}"
            )
            return
        try:
            if len(what_name) > 32:
                await ctx.followup.send("Error: The name cannot exceed 32 chareacter")
                return
            await self.client.user.edit(username=what_name)
            await ctx.followup.send(f"Bot name successfully changed to : {what_name}")
        except discord.HTTPException as e:
            await ctx.followup.send(f"Failed to change bot name: {e}")
        except Exception as e:
            await ctx.followup.send(f"An unexpected error occurred: {e}")

async def setup(client):
    await client.add_cog(change_name_(client))