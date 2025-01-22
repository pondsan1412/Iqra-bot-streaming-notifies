import discord
from src.client.logic import sign_up

class signup_button_viewer(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=86400)

    @discord.ui.button(label="Vote", style=discord.ButtonStyle.green)
    async def vote(self, ctx:discord.Interaction, button: discord.ui.Button):
        await sign_up.sign_people(ctx)

    @discord.ui.button(label="spoil-list", style=discord.ButtonStyle.gray)
    async def spoillist(self, ctx:discord.Interaction, button: discord.ui.Button):
        await ctx.message.reply(content=f"{sign_up.spoil_people()}")