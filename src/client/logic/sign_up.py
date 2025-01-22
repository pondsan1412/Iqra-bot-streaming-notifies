import discord
import asyncio

#List of people
people = []

async def sign_people(ctx:discord.Interaction):
    """
    to sign people in list who ever click the button will sign up like mogi
    """
    try:
        global people

        if len(people) >=3:
            await ctx.followup.send("no more signup It's  full!")
            await asyncio.sleep(2)
            sorted = sorted(people)
            format_name = "\n".join([f"{i+1}. {name}" for i, name in enumerate(people)])
            await ctx.followup.send(content=f"List of people signup {format_name}")
        else:
            if ctx.user.name in people:
                await ctx.message.reply("you already sign up!", delete_after=10)
                return
            else:
                people.append(ctx.user.name)
                await ctx.response.edit_message(content=f"people signed up: {len(people)}")
    except Exception as e:
        await ctx.message.reply(f"something went wrong with: {e}")
        
def spoil_people():
    return "\n".join([f"{i+1}. {name}" for i, name in enumerate(people)])
