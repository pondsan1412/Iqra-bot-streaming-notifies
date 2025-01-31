import discord
import random

class Count:
    def __init__(self, count:int):
        """
        count: int
            the number of messages
        """
        self.count = count

    async def counting(self, message:discord.Message):
        """count the number of messages"""
        # counting number and + 1 every 5 user.message
        if message.channel.id == 1318407673120690258:
            if not message.content.isdigit():
                return
            async for message in message.channel.history(limit=1):
                self.count +=1
                random_between10 = random.randint(1,10)
                int_msg = int(message.content)
                if self.count >= random_between10:
                    self.count = 0
                    await message.channel.send(f"{int_msg+1}")
                    await message.author.send(f"{message.author.mention} You are Rickrolled! the number you sent in <#1318407673120690258> is {int_msg}\n https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    