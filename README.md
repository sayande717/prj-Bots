To clone this repository to your local system, run:

```bash
# HTTPS
git clone https://github.com/sayande717/prj-discord_bot.git
```
## Objective
- To build a Discord bot based on Python.
- Functions of the bot:
    - Perform calculations in a specific channel.
    - Generate random numbers.
    - Provide context-aware help based on the channel where it is invoked.

## Tech Stack

![Python](https://img.shields.io/badge/Python-FFFFFF?style=flat-square&logo=python&logoColor=FFFFFF&color=3776AB)
![Discord.py](https://img.shields.io/badge/Discord.py-FFFFFF?style=flat-square&logo=discord&logoColor=FFFFFF&color=5865F2)

## Install (Arch Linux)
- Discord py:
    ```bash
    # Using an AUR Helper:
    paru -S python-discord
    # Manually:
    git clone https://aur.archlinux.org/python-discord-py.git
    cd python-discord-py
    makepkg -si
    ```
- Python-dotenv:
    ```
    pacman -S python-dotenv
    ```
## Run
- Go to [Discord Developer Portal](https://discord.com/developers/applications).
- Create a `New Application`.
- Go to the `Bot` section & create a new bot.
- Provide these permissions to the bot:
    - `Privileged Gateway Intents` -> `Message Content Intent`
- Add the bot to your Discord server:
    - Go to `OAuth2`
    - Select `URL Generator`
    - Check `bot` in the `scopes` list.
    - Copy the URL.
    - Paste it in a new tab, and add the bot.
- Copy the bot token.
- Put the token in `.env` in the project's root directory.
    ```zsh
    ➜  echo "bot=BOT_TOKEN_HERE" >> .env
    ```
- Run the bot:
    ```zsh
    # If python = python 3+
    python bot.py
    # If python3 = python 3+
    python3 bot.py
    ```
