import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from helper import *
load_dotenv()

# Global Environment Variables
SERVER_ID = int(os.getenv('SERVER_ID')) # type: ignore

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your commands"))
    await bot.tree.sync(guild=discord.Object(id=SERVER_ID))
    print(f"Commands Bot: Logged in")


"""
Command: `/ping`
Utility: Pings a given IP address and returns the round-trip time in milliseconds as a string.
Input: IP address (default: "1.1.1.1")
Output: "Latency: **XX ms**" or "Latency: **-1 ms**"
"""
@bot.tree.command(guild=discord.Object(id=SERVER_ID), name="ping", description="Check if the bot is online")
async def ip_ping(interaction: discord.Interaction,
    ip_address: str = "1.1.1.1" # str = "1.1.1.1" assigns a default value, and makes input optional.
):
    output_list = helper_wan_ping(ip_address)
    output_str = f"Latency: **{output_list[0]}** ms"
    await interaction.response.send_message(output_str)


"""
Command: `/wan_speed_ondemand`
Utility: Check the WAN speed, on-demand.
Input: null
Output:
```
Date: **XX.XX.XXXX** | Time: **XX:XX**
Latency: **XX.XXX ms**
Upload: **XXX.XX Mbps**
Download: **XXX.XX Mbps**
```
"""
@bot.tree.command(guild=discord.Object(id=SERVER_ID), name="wan_speed", description="Check the Internet upstream speed")
async def wan_speed_ondemand(interaction: discord.Interaction,
    server_id: str = os.getenv('speedtest_SERVER_ID') # type: ignore
    ):
    # Defer the response to indicate that the bot is processing the command
    await interaction.response.defer(thinking=True)
    output_list = helper_wan_speed_ondemand(server_id)
    output_str = (
        f"Date: {output_list[0]} | Time: {output_list[1]}\n"
        f"Latency: {output_list[2]}\n"
        f"Upload: {output_list[3]}\n"
        f"Download: {output_list[4]}"
        )
    await interaction.followup.send(output_str)

"""
Command: `/status_dns`
Utility: Checks the status of local/upstream DNS servers.
Input: Server Type:
    - "lan": Local DNS servers
    - "wan": Upstream DNS servers
Output:
    - "lan":
        ```
        ## Local DNS Status:
        Server-0: :green_circle:
        Server-1: :green_circle:
        Server-2: :red_circle:
        ```
    - "wan":
        ```
        ## Upstream DNS Status:
        Server-0: :green_circle:
        Server-1: :green_circle:
        ```
"""

@bot.tree.command(guild=discord.Object(id=SERVER_ID), name="status_dns", description="Check if the DNS servers are responding")
async def status_dns(interaction: discord.Interaction,
                     server_type: str = "lan"):
    await interaction.response.defer(thinking=True)
    output_list = helper_dns_status(server_type)
    if server_type == "lan":
        output_str = "## Local DNS Status:\n" + "\n".join(f"- {line}" for line in output_list)
    elif server_type == "wan":
        output_str = "## Upstream DNS Status:\n" + "\n".join(f"- {line}" for line in output_list)
    else:
        output_str = "-1"
    await interaction.followup.send(output_str)

bot.run(os.getenv('COMMANDS_BOT_TOKEN')) # type: ignore
