import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from helper import *
import subprocess
import subprocess
import asyncio
from datetime import datetime
load_dotenv()

# Global Environment Variables
BOT_TOKEN = os.getenv('NOTIFICATIONS_BOT_TOKEN')
SERVER_ID = int(os.getenv('SERVER_ID')) # type: ignore

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

"""
Function: `on_ready()`
Utility: Called when the bot has successfully connected to Discord and is ready.
"""

@bot.event
async def on_ready():
    hostname = subprocess.check_output(["hostnamectl", "hostname"]).decode().strip()
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=hostname))
    await bot.tree.sync(guild=discord.Object(id=SERVER_ID))

    # Background tasks START
    # wan_speed_periodic.start()
    server_status_periodic.start()
    # Background tasks END

    print(f"Notification Bot: Logged in")


"""
Function: `wan_speed_periodic()`
Interval: Every 3 hours 45 minutes (13500 seconds)
Utility: Periodically checks for new speed test results in a CSV file and sends updates to a Discord channel.
Input: Reads from "./helper/speedtest_results.csv"
Output: Sends formatted speed test results to the specified Discord channel
```
Date: DD.MM.YYYY | Time: HH:MM
Latency: **XX ms**
Upload: **XXX.XX Mbps**
Download: **XXX.XX Mbps**
```
"""
target_wan_speed_csv = "./helper/speedtest_periodic.csv"
last_seen_lines = helper_wan_speed_periodic(target_wan_speed_csv)

@tasks.loop(seconds=13500)
async def wan_speed_periodic():
    global last_seen_lines
    global target_wan_speed_csv
    with open(target_wan_speed_csv, "r") as f:
        lines = set(f.readlines())
    new_lines = lines - last_seen_lines
    if new_lines:
        channel = bot.get_channel(int(os.getenv('CHANNEL_ID_bot_notifications_vlan-0_status')))  # type: ignore
        for line in new_lines:
            # Matches with format on CSV: date,time,latency,upload,download
            date, time, latency, upload, download = line.strip().split(",")
            output_str = (
                f"Date: {date} | Time: {time}\n"
                f"Latency: {latency} ms\n"
                f"Upload: {upload} Mbps\n"
                f"Download: {download} Mbps"
            )
            await channel.send(output_str) # type: ignore
        last_seen_lines = lines

"""
Function: `server_status_periodic()`
Interval: Every 30 seconds
Utility: 
- Checks the online status of multiple servers by pinging their VPN IP addresses.
- If a server's status changes (online/offline), sends a formatted notification to the specified Discord channel.
Input: null
Output:
### DD.MM.YYYY at HH:MM:SS:
> Server-**X** is :green_circle: 
*or*
> Server-**X** is :red_circle:
"""

SERVER_COUNT = int(os.getenv('SERVER_COUNT')) # type: ignore
current_status = [-1] * SERVER_COUNT
@tasks.loop(seconds=30)
async def server_status_periodic():
    global current_status
    channel = bot.get_channel(int(os.getenv('CHANNEL_ID_bot_notifications_vlan-0_status'))) #type: ignore
    for i in range(SERVER_COUNT): # type: ignore
        host = os.getenv(f'ID_SERVER_TAILSCALE-{i}')
        try:
            proc = await asyncio.create_subprocess_exec(
            "ping", "-c", "3", "-W", "2", host,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            )
            await asyncio.wait_for(proc.wait(), timeout=5)
            returncode = proc.returncode
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            returncode = 1
        if returncode != current_status[i]:
            now = datetime.now()
            date_str = now.strftime("%d.%m.%Y")
            time_str = now.strftime("%H:%M:%S")
            await channel.send(f"\n### {date_str} at {time_str}:\n> Server-**{i}** {'is :green_circle:' if returncode == 0 else 'is :red_circle:'}")
        current_status[i] = returncode

bot.run(BOT_TOKEN) # type: ignore
