import discord

def intentAll():
    """return all intent"""
    return discord.Intents.all()

def intentLimit(**kwargs):
    """specific intent"""
    intents = discord.Intents.default()
    for key, value in kwargs.items():
        if hasattr(intents, key):
            setattr(intents, key, value)
    return intents
