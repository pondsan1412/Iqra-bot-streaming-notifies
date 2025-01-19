from discord.ext import commands
import discord.app_commands as app
from src.module import connection
from src.client import embed
import discord

class ping(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @app.command()
    async def ping(self, interaction:discord.Interaction):
        """check host between client and discord server"""
        try:
            if interaction:
                value = connection.check_ping(url="https://discord.com/")
                await interaction.response.send_message(embed=embed.fastEmbed(
                    name=interaction.user.name,
                    message=value
                ))
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")


async def setup(client):
    await client.add_cog(ping(client))