# SoupBot - Advanced Discord Crash Bot

![Version](https://img.shields.io/badge/version-1.0.0--beta-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

**SoupBot** - A powerful tool for destroying Discord servers with flexible functionality.

## ⚠️ Warning!
This bot is under development. This version is the first public beta test. Future versions will be more user-friendly and feature-rich.

## ✨ Features

- ***Server Destruction**: Destroys servers in seconds (this mode is highly configurable)
- **Kick/Ban**: With customizable delays
- **Channel Management**: Mass creation/deletion of channels
- **Role Management**: Create, assign, and delete roles
- **Security System**: Whitelist and ignore list
- **Detailed Statistics**: Track all bot actions
- **Colored Logging**: Customizable logging levels with colorama support
- **Stealth Mode**: No one will know who's doing it...
- **Auto-save**: Automatic saving of statistics and "trophies"
- **Configurability**: Flexible configuration through config file

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- Discord bot token
- Administrator permissions (in bot)

### Executable Version
Download the archive from GitHub, extract it, and run the exe file.

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Quvis/FuckDiscord.git
   cd FuckDiscord
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # For Windows
   .venv\Scripts\activate
   
   # For Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot**
   - Open `config/config.ini`
   - Set your Discord token
   - Configure whitelist and other parameters (more details below)

5. **Run the bot**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Complete Configuration Documentation

| Section | Parameter | Description | Default Value |
|---------|-----------|-------------|---------------|
| **Auth** | Token | Discord bot token | `123` (change this!) |
| | Tester | Tester mode | `False` |
| | Version | Bot version | `1.3.1-beta` |
| **Lists** | Whitelist | Trusted users list | `[]` |
| | Ignorelist | Protected users list | `[]` |
| **Logging** | LogStatus | Enable logging | `True` |
| | LogType | Log detail level | `3` |
| | Trophy | Create trophies | `True` |
| **Status** | BotStatus | Bot status | `online` |
| | BotPresenceType | Activity type | `watching` |
| | BotPresence | Activity text | `The end is a near...` |
| **SoupDay** | Method | Punishment method | `kick` |
| | ChangeServerIcon | Change server icon | `True` |
| | ChangeServerName | Change server name | `True` |
| **Settings** | StealthMode | Stealth mode | `True` |
| | KickMessage | Message before kick | `False` |
| **Delays** | CustomDelays | Custom delays | `False` |
| **Testing** | SpyModeStatus | Spy mode status | `False` |
| | Statistic | Track statistics | `True` |

Sorry for the uninformative table... I'll make it more useful in the next version.

## Commands

### Main Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `!spam <message>` | Start spamming messages | `!spam Hello World` |
| `!stop_spam` | Stop spam | `!stop_spam` |
| `!give_role <user_id> <role_id>` | Give role | `!give_role 123456 789012` |
| `!del_role <user_id> <role_id>` | Remove role | `!del_role 123456 789012` |
| `!make_role <name> <give>` | Create role | `!make_role Admin 1` |
| `!soupday` | Activate "Soup Day" protocol | `!soupday` |

### Informational Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `!stats` | Show statistics | `!stats` |
| `!save_stats` | Save statistics | `!save_stats` |
| `!log_test` | Test logging system | `!log_test` |

### "Soup Day" Protocol

The `!soupday` command performs the following actions:
1. Mass kick all users (except whitelist)
2. Delete all channels
3. Delete all roles (except @everyone)
4. Change server icon
5. Rename server (if configured)
6. Create "trophy" with detailed information
THIS OPTION IS CONFIGURABLE AND ONLY DOES WHAT YOU NEED!

## 📊 Logging System

### Logging Levels

| Level | Description |
|-------|-------------|
| 0 | No logs |
| 1 | Errors only |
| 2 | Basic logs |
| 3 | Extended logs |
| 4 | Full logs |

### Log Examples

```bash
[14:30:25] [BOT] SoupBot#1234 activated!
[14:30:25] [INFO] Bot version: 1.3.1-beta
[14:30:25] [INFO] Stealth mode: ON
[14:31:10] [COMMAND] Spam started by user Admin#0001
[14:32:00] [CRITICAL] ACTIVATION OF 'SOUP DAY' PROTOCOL
```

## 🔒 Security

### Whitelist System
- Only users in the whitelist can use commands
- User IDs are specified in `config/config.ini`
- Format: `[1234567890, 9876543210]`

### Ignore List
Same as whitelist, but without command execution permissions.

## 🐛 Common Issues

**Issue**: Bot doesn't start
```
Solution: Check token in config.ini and internet connection
```

**Issue**: Commands don't work
```
Solution: Check whitelist and bot permissions on the server
```

**Issue**: Errors when deleting channels
```
Solution: Make sure the bot has administrator permissions
```

### Error Logs

Logs are saved in the console. For detailed analysis:
1. Set `LogType = 4` in config
2. Restart the bot
3. Reproduce the error
4. Copy logs from console

## 📄 License

This project is distributed under the MIT license. See the `LICENSE` file for details.

---

**Warning**: This bot is intended for legal use on servers where you have appropriate permissions. The developer is not responsible for illegal use.

**Support**: For questions and support, refer to Issues on GitHub or contact the creator on Discord.

**Updates**: Follow updates on GitHub for new features and bug fixes.

**Security**: Security vulnerability reports are accepted confidentially.
