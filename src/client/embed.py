import discord

def fastEmbed(name:str=None, message:str = "None"):
    """only text in field"""
    embed = discord.Embed(title=name)
    embed.add_field(
        name="Field",
        value=message
    )
    return embed
