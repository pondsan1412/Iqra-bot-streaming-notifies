import discord


class view_request_accept(discord.ui.View):
    def __init__(self, user, guild, callback=None):
        super().__init__(timeout=None)
        self.user = user  # ผู้ใช้ที่เรียกคำสั่ง register
        self.guild = guild  # Guild ที่ต้องเพิ่ม role
        self.callback = callback  # ฟังก์ชัน callback เพื่อส่งสถานะกลับ

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(self.guild.roles, name="Eskimo's")
        if not role:
            await interaction.response.send_message("Role 'Eskimo's' not found in the server.", ephemeral=True)
            return

        member = self.guild.get_member(self.user.id)
        if not member:
            await interaction.response.send_message("User not found in the server.", ephemeral=True)
            return

        try:
            # เพิ่ม role ให้ผู้ใช้
            await member.add_roles(role)
            await interaction.response.send_message(f"Successfully added role 'Eskimo's' to {member.mention}.", ephemeral=True)
            await member.remove_roles(discord.utils.get(self.guild.roles, name="unregistered"))
            # เรียก callback เพื่อส่งสถานะกลับ
            if self.callback:
                self.callback(True)

            # หยุด view
            self.stop()
        except discord.Forbidden:
            await interaction.response.send_message("Bot does not have permission to add roles.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @discord.ui.button(label="Refuse", style=discord.ButtonStyle.danger)
    async def refuse(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = self.guild.get_member(self.user.id)
        if not member:
            await interaction.response.send_message("User not found in the server.", ephemeral=True)
            return

        try:
            # เตะผู้ใช้ออกจากเซิร์ฟเวอร์
            await member.kick(reason="Request to join server was refused.")
            await interaction.response.send_message(
                f"Request to join by {self.user.mention} has been refused and the user was kicked.", ephemeral=True
            )

            # เรียก callback เพื่อส่งสถานะปฏิเสธกลับ
            if self.callback:
                self.callback(False)

            # หยุด view
            self.stop()
        except discord.Forbidden:
            await interaction.response.send_message("Bot does not have permission to kick this user.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
