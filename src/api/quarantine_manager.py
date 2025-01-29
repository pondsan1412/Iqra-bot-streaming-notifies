import asyncio
import discord
from src.api.iicemkdatabase import get_quarantine_remaining_time, get_quarantine_messages
from src.module.dc import clientdc
import os
from dotenv import load_dotenv

load_dotenv()

async def update_quarantine_embeds():
    """Automatically update quarantine embeds using stored message IDs."""
    while True:
        cliend_guild = discord.utils.get(clientdc.guilds, name=os.getenv("GUILD_NAME"))
        if not cliend_guild:
            print("❌ Guild not found. Check GUILD_NAME in .env file.")
            return

        quarantine_messages = get_quarantine_messages()

        for record in quarantine_messages:
            user_id, message_id, channel_id = record["user_id"], record["message_id"], record["channel_id"]

            channel = cliend_guild.get_channel(channel_id)
            if not channel:
                continue

            try:
                message = await channel.fetch_message(message_id)
            except discord.NotFound:
                continue  # Skip if the message is deleted

            remaining_time = get_quarantine_remaining_time(user_id)

            embed = message.embeds[0]
            embed.set_field_at(0, name="⏳ Remaining Time", value=remaining_time, inline=False)
            await message.edit(embed=embed)

        await asyncio.sleep(3600)  # Update every hour
