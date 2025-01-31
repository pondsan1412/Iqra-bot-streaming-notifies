import discord
from discord.ext import commands
from src.client import intent
import datetime
from dateutil import tz
import os

class client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intent.intentAll(),
            help_command=None
        )

    #@event listener when bot is start up
    async def on_ready(self):
        BBK = tz.gettz('Thailand / Bangkok')
        print(f"bot started up at: {datetime.datetime.now(tz=BBK)}")
        

    async def setup_hook(self):
        """
        Dynamically load all Cogs from 'commands' and 'event-listener' directories
        and sync application commands (slash commands).
        """
        base_path = "src.cog"
        categories = ["commands", "event-listener","autotask"]
        
        # Dynamically load all Cogs
        for category in categories:
            path = os.path.join(base_path.replace(".", "/"), category)
            for filename in os.listdir(path):
                if filename.endswith(".py") and not filename.startswith("__"):
                    cog_name = f"{base_path}.{category}.{filename[:-3]}"
                    try:
                        await self.load_extension(cog_name)
                        print(f"Loaded Cog: {cog_name}")
                    except Exception as e:
                        print(f"Failed to load Cog: {cog_name} - {e}")

        # Sync application commands
        try:
            await self.tree.sync()
            print("Application commands synced successfully!")
        except Exception as e:
            print(f"Failed to sync application commands: {e}")

        print("Cogs loaded and commands synced successfully.")
