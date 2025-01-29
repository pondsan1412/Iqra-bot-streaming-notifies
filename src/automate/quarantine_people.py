from src.module import dc
import os
from dotenv import load_dotenv
from src.api.iicemkdatabase import check_unquarantine_users, remove_from_quarantine, get_quarantine_remaining_time, save_quarantine, store_quarantine_message
from src.api.quarantine_manager import update_quarantine_embeds

load_dotenv()

clientdc = dc.cli

async def monitorDangerousPerson(cli: clientdc.Client, user: clientdc.Member):
    """Quarantine a dangerous user (if needed)."""

    cliend_guild = clientdc.utils.get(cli.guilds, name=os.getenv("GUILD_NAME"))
    quarantine_role = clientdc.utils.get(cliend_guild.roles, name=os.getenv("QUARANTINE_ROLE_NAME"))
    report_ch = clientdc.utils.get(cliend_guild.text_channels, name=os.getenv("REPORT_CHANNEL_NAME"))

    if not quarantine_role:
        quarantine_role = await cliend_guild.create_role(name="Quarantine", color=clientdc.Color.red())

    # Skip if user is already quarantined
    if quarantine_role in user.roles:
        return  

    # Check if user should be quarantined
    account_age_days = (clientdc.utils.utcnow() - user.created_at).days
    no_profile_picture = user.avatar is None

    if account_age_days < 30 or no_profile_picture:
        await user.add_roles(quarantine_role)
        reason = "Account < 30 days" if account_age_days < 30 else "No profile picture"
        await user.send(f"You have been quarantined. Reason: {reason}")

        # Save to database
        save_quarantine(user.id, user.name, reason)

        # Send quarantine embed
        embed = clientdc.Embed(title=f"🚨 {user.name} Quarantined", color=clientdc.Color.red())
        embed.add_field(name="⏳ Remaining Time", value=get_quarantine_remaining_time(user.id), inline=False)
        embed.set_footer(text=f"User ID: {user.id}")

        msg = await report_ch.send(embed=embed)

        # Store the embed message ID
        store_quarantine_message(user.id, msg.id, report_ch.id)

async def unquarantinePerson(cli: clientdc.Client):
    """
    Automatically unquarantine users after 14 days.
    - Checks the database for users past their quarantine time.
    - Removes the quarantine role from them in Discord.
    - Deletes them from the quarantine table.
    - Sends a notification in the report channel.
    """

    cliend_guild = clientdc.utils.get(cli.guilds, name=os.getenv("GUILD_NAME"))
    if not cliend_guild:
        print("❌ Guild not found. Check GUILD_NAME in .env file.")
        return

    quarantine_role = clientdc.utils.get(cliend_guild.roles, name=os.getenv("QUARANTINE_ROLE_NAME"))
    if not quarantine_role:
        print("⚠️ No quarantine role found in the server.")
        return

    report_ch = clientdc.utils.get(cliend_guild.text_channels, name=os.getenv("REPORT_CHANNEL_NAME"))
    if not report_ch:
        report_ch = await cliend_guild.create_text_channel(name=os.getenv("REPORT_CHANNEL_NAME"))

    # Fetch users who should be unquarantined
    unquarantine_list = check_unquarantine_users()
    if not unquarantine_list:
        return

    for user_data in unquarantine_list:
        user_id = user_data["user_id"]
        username = user_data["username"]

        # Fetch user from Discord server
        user = cliend_guild.get_member(user_id)
        if user and quarantine_role in user.roles:
            await user.remove_roles(quarantine_role)
            await user.send("You have been removed from quarantine after 14 days.")
            await report_ch.send(f"{user.mention} has been unquarantined automatically.")

        # Remove from database
        remove_from_quarantine(user_id)

    print("✅ Unquarantine process completed.")

async def check_existing_members():
    """Check all members in the server when the bot starts."""
    await clientdc.wait_until_ready()  # Ensure bot is ready before running

    cliend_guild = clientdc.utils.get(clientdc.guilds, name=os.getenv("GUILD_NAME"))
    if not cliend_guild:
        print("❌ Guild not found. Check GUILD_NAME in .env file.")
        return

    print("🔍 Checking all existing members for quarantine conditions...")

    for member in cliend_guild.members:
        await monitorDangerousPerson(clientdc, member)  # Check each member

    print("✅ Finished checking existing members.")