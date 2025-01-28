import os
import discord
from dotenv import load_dotenv

async def fetch_passkey(client: discord.Client):
    """Get passkey in passkey channel and save it in instants."""
    load_dotenv()
    passkey_channel_id = os.getenv("PASSKEY_CH")
    if not passkey_channel_id:
        raise ValueError("PASSKEY_CH environment variable not set.")
    
    channel = client.get_channel(int(passkey_channel_id))
    if not channel:
        raise ValueError(f"Channel with ID {passkey_channel_id} not found.")
    
    # Fetch the last message in the channel
    async for message in channel.history(limit=1):
        return message.content
    
    raise ValueError("No messages found in the passkey channel.")

