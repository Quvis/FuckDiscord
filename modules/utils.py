import json
import os
from datetime import datetime
from typing import Dict, Any
from colorama import init, Fore, Style

from init import *

# Initialize colorama
init(autoreset=True)

# ===== STATISTICS =====
stats = {
    "messages_sent": 0,
    "members_kicked": 0,
    "members_banned": 0,
    "channels_deleted": 0,
    "channels_created": 0,
    "roles_deleted": 0,
    "roles_created": 0,
    "servers_crashed": 0,
    "spam_messages": 0,
    "commands_executed": 0
}


def log_event(level: str, message: str, module: str = "SYSTEM"):
    """Log events with color coding"""
    if not LogStatus:
        return

    timestamp = datetime.now().strftime("%H:%M:%S")
    level_colors = {
        "INFO": GREEN,
        "WARNING": YELLOW,
        "ERROR": RED,
        "CRITICAL": RED + Style.BRIGHT,
        "DEBUG": CYAN,
        "SUCCESS": GREEN + Style.BRIGHT,
        "BOT": MAGENTA,
        "COMMAND": BLUE,
        "EVENT": CYAN,
    }

    level_color = level_colors.get(level, RESET)

    # Logging level
    if LogType == 0:  # No logs
        return
    elif LogType == 1:  # Only errors
        if level not in ["ERROR", "CRITICAL"]:
            return
    elif LogType == 2:  # Basic logs
        if level in ["DEBUG"]:
            return
    elif LogType == 3:  # Extended logs
        if level in ["DEBUG", "SUCCESS"]:
            return

    print(
        f"{BLUE}[{timestamp}]{RESET} {level_color}[{level}]{RESET} {YELLOW}[{module}]{RESET} {message}")


def update_statistic(stat_name: str, value: int = 1):
    """Update statistics"""
    if stat_name in stats:
        stats[stat_name] += value
        if Statistic and TesterMode:
            log_event("DEBUG", f"Statistic '{stat_name}' updated: {stats[stat_name]}", "STATS")


def save_statistics():
    """Save statistics to file"""
    try:
        stats_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        log_event("SUCCESS", "Statistics saved", "STATS")
    except Exception as e:
        log_event("ERROR", f"Error saving statistics: {e}", "STATS")


def load_statistics():
    """Load statistics from file"""
    try:
        stats_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'stats.json')
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                loaded_stats = json.load(f)
                stats.update(loaded_stats)
            log_event("INFO", "Statistics loaded", "STATS")
    except Exception as e:
        log_event("WARNING", f"Error loading statistics: {e}", "STATS")


def get_stats() -> Dict[str, Any]:
    """Get current statistics"""
    return stats.copy()


def create_trophy(server_name: str, server_id: int, terminated_by: str, terminated_by_id: int):
    """Create trophy"""
    if not Trophy:
        return

    try:
        trophy_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'trophy.json')
        trophy_data = {
            "server_name": server_name,
            "server_id": server_id,
            "terminated_by": terminated_by,
            "terminated_by_id": terminated_by_id,
            "termination_date": datetime.now().isoformat(),
            "statistics": stats.copy()
        }
        with open(trophy_file, 'w', encoding='utf-8') as f:
            json.dump(trophy_data, f, indent=4, ensure_ascii=False)
        log_event("SUCCESS", "Trophy created!", "TROPHY")
    except Exception as e:
        log_event("ERROR", f"Error creating trophy: {e}", "TROPHY")


# Load statistics on import
load_statistics()