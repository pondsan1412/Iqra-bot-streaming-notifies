import discord
import requests
from io import BytesIO

async def change_profile_picture(bot: discord.Client, image_url: str):
    """
    Changes the bot's profile picture from an image URL.

    Args:
        bot (discord.Client): The Discord bot client.
        image_url (str): URL of the image.

    Returns:
        str: Success message or error message.
    """
    try:
        # Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        # Load the image into BytesIO
        avatar_data = BytesIO(response.content)

        # Change the bot's avatar
        await bot.user.edit(avatar=avatar_data.read())
        return "Profile picture updated successfully!"
    except requests.exceptions.RequestException as req_err:
        return f"Failed to fetch image from URL: {req_err}"
    except discord.HTTPException as http_exc:
        return f"Discord HTTP error: {http_exc}"
    except Exception as e:
        return f"Unexpected error: {e}"
