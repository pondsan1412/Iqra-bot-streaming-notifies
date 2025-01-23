import discord
import os
from dotenv import load_dotenv

load_dotenv()

async def report_to_admin(ctx: discord.Client, cmd_used:str, author: str, content:str):
    """report to admin """
    if os.getenv("POND_ID"):
        report_ch = os.getenv("REPORT_CH")
        get_ch = ctx.get_channel(report_ch)
        embed = discord.Embed(
            title="Report To admin"
        )
        embed.add_field(name="Command used", value=f"{cmd_used}")
        embed.add_field(name="content they tried", value=f"{content}")
        embed.set_footer(text=f"author: {author}")
        await get_ch.send(embed=embed)
    else:
        return None

async def report_to_logCh(ctx: discord.Client, cmd_used:str, author: str, content:str):
    """report to log channel """
    if os.getenv("TEST_CH"):
        report_ch = int(os.getenv("TEST_CH"))

        get_ch = ctx.get_channel(report_ch)
        embed = discord.Embed(
            title="Report"
        )
        embed.add_field(name="Command used", value=f"{cmd_used}")
        embed.add_field(name="content they tried", value=f"{content}")
        embed.set_footer(text=f"author: {author}")
        await get_ch.send(embed=embed)
    else:
        return None
    

