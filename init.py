import os
import configparser
import json
import disnake
from disnake.ext import commands

# ===== CONFIGURATION =====
config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.ini')
config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')

# ===== AUTHORIZATION =====
Token = config.get("Auth", "Token")
TesterMode = config.getboolean("Auth", "Tester")
Version = config.get("Auth", "Version")
UserId = config.get("Auth", "UserId")

# ===== STATISTICS =====
Stats_MessagesSend = config.get("Stats", "MessagesSend")
Stats_MembersKicked = config.get("Stats", "MembersKicked")
Stats_MembersBanned = config.get("Stats", "MembersBanned")
Stats_ChannelsDelete = config.get("Stats", "ChannelsDelete")
Stats_ChannelsCreate = config.get("Stats", "ChannelsCreate")
Stats_ServersCrashed = config.get("Stats", "ServersCrashed")

# ===== LISTS =====
whit = json.loads(config.get("Lists", "Whitelist"))
ignore = json.loads(config.get("Lists", "Ignorelist"))

# ===== LOGGING =====
LogStatus = config.getboolean("Logging", "LogStatus")
LogType = config.getint("Logging", "LogType")
Trophy = config.getboolean("Logging", "Trophy")

# ===== STATUS =====
PRESENCE_STATUS_STR = config.get("Status", "BotStatus")
PRESENCE_TYPE_STR = config.get("Status", "BotPresenceType")
PRESENCE_TEXT = config.get("Status", "BotPresence")

# ===== SETTINGS =====
StealthMode = config.getboolean("Settings", "StealthMode")
HardStealthMode = config.getboolean("Settings", "HardStealthMode")
KickMessage = config.getboolean("Settings", "KickMessage")
EndChanel = config.getboolean("Settings", "EndChanel")
EndChanelName = config.get("Settings", "EndChanelName")

# ===== DELAYS =====
CustomDelays = config.getboolean("Delays", "CustomDelays")
BanDelay = config.getfloat("Delays", "BanDelay")
KickDelay = config.getfloat("Delays", "KickDelay")
SpamDelay = config.getfloat("Delays", "SpamDelay")
RoleSpamDelay = config.getfloat("Delays", "RoleSpamDelay")
ChanelSpamDelay = config.getfloat("Delays", "ChanelSpamDelay")
ChanelRemoveDelay = config.getfloat("Delays", "ChanelRemoveDelay")

# ===== TESTING =====
SpyModeStatus = config.getboolean("Testing", "SpyModeStatus")
Statistic = config.getboolean("Testing", "Statistic")

# ===== SOUP DAY =====
SoupDayMethod = config.get("SoupDay", "Method")
ChangeServerIcon = config.getboolean("SoupDay", "ChangeServerIcon")
ChangeServerName = config.getboolean("SoupDay", "ChangeServerName")
SoupDayServerName = config.get("SoupDay", "SoupDayServerName")
SoupDayKickMessage = config.getboolean("SoupDay", "SoupDayKickMessage")
SoupDayEndChanel = config.getboolean("SoupDay", "EndChanel")
SoupDayEndChanelName = config.get("SoupDay", "EndChanelName")
SoupDayMessage = config.get("SoupDay", "Message")

# ===== BOT INITIALIZATION =====
intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== STATUS CONVERSION =====
status_mapping = {
    "online": disnake.Status.online,
    "idle": disnake.Status.idle,
    "dnd": disnake.Status.dnd,
    "do_not_disturb": disnake.Status.dnd,
    "invisible": disnake.Status.invisible,
    "offline": disnake.Status.invisible,
}

activity_mapping = {
    "playing": disnake.ActivityType.playing,
    "streaming": disnake.ActivityType.streaming,
    "listening": disnake.ActivityType.listening,
    "watching": disnake.ActivityType.watching,
    "competing": disnake.ActivityType.competing,
    "custom": disnake.ActivityType.custom,
}

PRESENCE_STATUS = status_mapping.get(PRESENCE_STATUS_STR.lower(), disnake.Status.online)
PRESENCE_TYPE = activity_mapping.get(PRESENCE_TYPE_STR.lower(), disnake.ActivityType.watching)

# ===== LOADING ADDITIONAL FILES =====
# Loading logo
image_path = os.path.join(os.path.dirname(__file__), 'config', 'logo.png')

# Loading punishment message
text_dir = os.path.dirname(os.path.abspath(__file__))
text_path = os.path.join(text_dir, "config", "text.txt")
if os.path.exists(text_path):
    with open(text_path, "r", encoding="utf-8") as file:
        kick_message = file.read()
else:
    kick_message = "Punishment"


# ===== CONFIG VALIDATION =====
def validate_config():
    """Validate configuration"""
    errors = []

    # Token check
    if not Token:
        errors.append("Token not set!")

    # Lists check
    try:
        _ = json.loads(config.get("Lists", "Whitelist"))
        _ = json.loads(config.get("Lists", "Ignorelist"))
    except json.JSONDecodeError as e:
        errors.append(f"Error in list format: {e}")

    # LogType check
    if LogType not in range(0, 5):
        errors.append("LogType must be in range 0-4")

    # Status check
    if PRESENCE_STATUS_STR.lower() not in status_mapping:
        errors.append(f"Invalid bot status: {PRESENCE_STATUS_STR}")

    # Activity type check
    if PRESENCE_TYPE_STR.lower() not in activity_mapping:
        errors.append(f"Invalid activity type: {PRESENCE_TYPE_STR}")

    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    return True


# ===== CONSOLE COLORS (COLORAMA) =====
# Basic text colors
RED = "\033[91m"      # Red
GREEN = "\033[92m"    # Green
YELLOW = "\033[93m"   # Yellow
BLUE = "\033[94m"     # Blue
MAGENTA = "\033[95m"  # Magenta
CYAN = "\033[96m"     # Cyan
WHITE = "\033[97m"    # White
GRAY = "\033[90m"     # Gray

# Styles
BOLD = "\033[1m"      # Bold
DIM = "\033[2m"       # Dim
UNDERLINE = "\033[4m" # Underlined
RESET = "\033[0m"     # Reset styles

# Background colors (useless stuff)
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"

# ===== Shortcuts =====
R = RED
G = GREEN
Y = YELLOW
B = BLUE
C = CYAN
M = MAGENTA
W = WHITE

X = RESET

# Import for backward compatibility
try:
    from modules.utils import *
    from modules.actions import *
    from modules.security import *
except ImportError:
    print("Modules not yet initialized")