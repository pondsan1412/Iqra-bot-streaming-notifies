import discord

async def handle_offline(message: discord.Message):
    """
    Handles messages from users with 'offline' status in Discord.

    This function deletes the message sent by a user who has their
    Discord status set to 'offline' and sends a warning message
    to inform them about the restriction.

    Args:
        message (discord.Message): The message object received from Discord.

    Usage:
        Call this function inside an event listener for messages, such as:
        @bot.event
        async def on_message(message):
            await handle_offline(message)
    
    Notes:
        - This function assumes that the message object contains a valid 
          'author.status' property from Discord API.
        - Requires proper permissions to delete messages in the channel.
    """
    try:
        if message.author.status.value == "offline":
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, your status is set to `{message.author.status}`. "
                f"Please change it to something else to send messages."
            )
        else:
            return
    except Exception as e:
        await message.channel.send(f"Error: {e}")

