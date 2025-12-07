import disnake
from modules.utils import log_event
from init import *


def check_permissions(ctx) -> bool:
    if ctx.author.id in whit:
        return True

    if not StealthMode:
        try:
            from modules.utils import COLOR_RED, COLOR_RESET
            asyncio.create_task(ctx.send(f"{COLOR_RED}Access denied!{COLOR_RESET}"))
        except:
            pass

    log_event("WARNING", f"Unauthorized command attempt: {ctx.author} ({ctx.author.id})", "SECURITY")
    return False

# Check if user is in whitelist
def is_whitelisted(user_id: int) -> bool:
    return user_id in whit

# Check if user is in ignore list
def is_ignored(user_id: int) -> bool:
    return user_id in ignore


def can_target_member(member_id: int, executor_id: int) -> bool:
    # Executor must be in whitelist
    if executor_id not in whit:
        return False

    # Target must not be in whitelist
    if member_id in whit:
        return False

    # Target must not be in ignore list (unless it's soup day)
    from modules.actions import get_soup_mode
    if member_id in ignore and not get_soup_mode():
        return False

    return True