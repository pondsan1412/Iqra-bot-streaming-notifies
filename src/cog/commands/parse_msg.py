import discord
import discord.app_commands as app
from discord.ext import commands

class remove_msg(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @app.command()
    async def clear_channel(self, interaction: discord.Interaction):
        # ตรวจสอบว่าผู้ใช้มีสิทธิ์เป็น Admin หรือไม่
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("you dont have permission")
            return

        await interaction.response.send_message("delete all messege...")

        # ลบข้อความทั้งหมดใน channel
        deleted = await interaction.channel.purge()
        await interaction.followup.send(f"deleted all message {len(deleted)} successful")

async def setup(client):
    await client.add_cog(remove_msg(client))