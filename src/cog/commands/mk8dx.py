import discord
from discord.ext import commands
from discord import app_commands
from src.api import mk8dx_api
import asyncio

class mk8dx(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command()
    async def mmr(self, ctx:discord.Interaction, select_people: discord.Member, season: int = None):
        """
        show specific player mmr
        """
        await ctx.response.defer(thinking=True)
        try:
            if select_people:
                mmr, name, rank, seasons= mk8dx_api.previous_season_stats(select_people.id, season)
                embed = discord.Embed(
                    title=f"{select_people.name}'s short info"
                )
                embed.add_field(name=f"{name} season: {seasons}", value=f"mmr: {mmr}\nranking: {rank}")
                embed.set_thumbnail(url=select_people.avatar.url if select_people.avatar else "https://oyster.ignimgs.com/mediawiki/apis.ign.com/mario-kart-for-wii-u/f/f0/Mk8iconroy.png?width=325")
                await ctx.followup.send(embed=embed)
            else:
                await ctx.followup.send("error")
        except discord.Forbidden as dc:
            await ctx.followup.send(f"discord Forbidden: {dc}")
        except Exception as e:
            await ctx.followup.send(f"error: {e}\n info not found\nthis user probably not playing mk8dx")



    @app_commands.command()
    async def allmmr(self, interaction: discord.Interaction):
        """
        This command shows all people's MMR in the server.
        """
        await interaction.response.defer(thinking=True)

        try:
            # ดึงสมาชิกในเซิร์ฟเวอร์ (ยกเว้น Bot)
            members = [member for member in interaction.guild.members if not member.bot]

            # เรียกฟังก์ชัน async_stats_mmr_and_ranked สำหรับแต่ละสมาชิก
            tasks = [mk8dx_api.async_stats_mmr_and_ranked(member.id) for member in members]
            results = await asyncio.gather(*tasks)

            # กรองผลลัพธ์: เอาเฉพาะผู้ที่มี MMR ไม่ใช่ "N/A"
            valid_results = [res for res in results if res["mmr"] != "N/A"]

            # เรียงลำดับผลลัพธ์ตาม MMR (มากไปน้อย)
            sorted_results = sorted(
                valid_results, key=lambda x: x["mmr"], reverse=True
            )

            # เตรียมข้อมูลในรูปแบบบรรทัดเดียว
            description = "\n".join(
                f"{i + 1}. {player['name']} ({player['rank']}) - MMR: {player['mmr']} <@{player['id']}>"
                for i, player in enumerate(sorted_results)
            )

            # สร้าง Embed
            embed = discord.Embed(
                title="Server MMR Rankings",
                description=description,
                color=discord.Color.blue()
            )

            # ส่ง Embed
            await interaction.followup.send(embed=embed)

        except Exception as e:
            # แสดง Error
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"An error occurred while fetching MMR data: {str(e)}",
                    color=discord.Color.red()
                )
            )


async def setup(client):
    await client.add_cog(mk8dx(client))

   