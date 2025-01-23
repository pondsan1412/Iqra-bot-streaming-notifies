import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import src.client.logic.views.accept_role as accept_role

load_dotenv()

async def request_to_accept_role(client: discord.Client, ctx: discord.Interaction, callback=None):
    iqra_id = os.getenv("IQRA_ID")

    if not iqra_id:
        print("POND_ID ไม่ได้กำหนดใน .env")
        return

    try:
        admin_user = await client.fetch_user(int(iqra_id))
    except ValueError:
        print("IQRA_ID ไม่ใช่ตัวเลข")
        return
    except discord.NotFound:
        print(f"ไม่พบผู้ใช้ที่มี ID {iqra_id}")
        return

    embed = discord.Embed(
        title="Request to join IceMK server",
        color=discord.Color.green()
    )
    embed.add_field(
        name="This user wants to join your server",
        value=f"""
name: {ctx.user.name} {ctx.user.mention}
account birth: {ctx.user.created_at}
discord id: {ctx.user.id}
"""
    )
    embed.set_image(
        url=ctx.user.avatar.url if ctx.user.avatar else "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSuV3pnrrgeSNYPADFteFSiKUUFgD-04hYBA&s"
    )

    # สร้าง view พร้อม callback
    view = accept_role.view_request_accept(user=ctx.user, guild=ctx.guild, callback=callback)

    try:
        await admin_user.send(embed=embed, view=view)
        print(f"ส่งข้อความถึง {admin_user.name} สำเร็จ")
    except discord.Forbidden:
        print("บอทไม่มีสิทธิ์ส่งข้อความถึงผู้ใช้นี้")
    except discord.HTTPException as e:
        print(f"เกิดข้อผิดพลาดในการส่งข้อความ: {e}")


