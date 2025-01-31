import discord

def fastEmbed(name:str=None, message:str = "None"):
    """only text in field"""
    embed = discord.Embed(title=name)
    embed.add_field(
        name="Field",
        value=message
    )
    return embed


def rankEmbed(rankname: str):
    """return discord.Color based on rankname"""
    rankname = ''.join(filter(str.isalpha, rankname))  # Extract only alphabetic characters
    if rankname == "Iron":
        return discord.Color.default()
    elif rankname == "Bronze":
        return discord.Color.dark_gold()
    elif rankname == "Silver":
        return discord.Color.light_gray()
    elif rankname == "Gold":
        return discord.Color.gold()
    elif rankname == "Platinum":
        return discord.Color.blue()
    elif rankname == "Sapphire":
        return discord.Color.dark_blue()
    elif rankname == "Ruby":
        return discord.Color.red()
    elif rankname == "Diamond":
        return discord.Color.og_blurple()
    elif rankname == "Master":
        return discord.Color.yellow()
    