import asyncio
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot, Chat
from telegram.ext import Application

load_dotenv()

# Global Environment Variables
BOT_TOKEN = os.getenv('TEST_BOT-TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID_bot-test_text')  # type: ignore

# Initialize bot
application = Application.builder().token(BOT_TOKEN).build()
bot = application.bot

"""
Function: `on_ready()`
Utility:  Called when the bot has successfully connected to Telegram and is ready. 
"""

async def on_ready():
    hostname = subprocess.check_output(["hostnamectl", "hostname"]).decode().strip()
    try:
        await bot.set_my_description(f"Status monitoring bot running on {hostname}")
    except Exception as e:
        print(f"Could not set bot description: {e}")

    # Background tasks START
    await server_status_periodic()
    # Background tasks END

    print(f"Notification Bot: Connected")

"""
Function: `server_status_periodic()`
Interval: Every 30 seconds
Utility: 
- Checks the online status of multiple servers by pinging their VPN IP addresses.
- If a server's status changes (online/offline), sends a formatted notification to the specified Telegram chat.
Input: null
Output:
DD.MM.YYYY at HH:MM:SS:
Server-X is 🟢 (online)
*or*
Server-X is 🔴 (offline)
"""

SERVER_COUNT = int(os.getenv('SERVER_COUNT'))  # type: ignore
current_status = [-1] * SERVER_COUNT

async def server_status_periodic():
    global current_status
    while True:
        try:
            for i in range(SERVER_COUNT):  # type: ignore
                host = os.getenv(f'ID_SERVER_TAILSCALE-{i}')
                try: 
                    proc = await asyncio.create_subprocess_exec(
                        "ping", "-c", "3", "-W", "2", host,
                        stdout=subprocess. DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    await asyncio. wait_for(proc.wait(), timeout=5)
                    returncode = proc.returncode
                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.wait()
                    returncode = 1

                if returncode != current_status[i]:
                    now = datetime.now()
                    date_str = now.strftime("%d.%m.%Y")
                    time_str = now.strftime("%H:%M:%S")
                    status = "🟢" if returncode == 0 else "🔴"
                    

                    message = f"{date_str} at {time_str}\n<strong>Server-{i}</strong> is {status}"
                    try:
                        await bot.send_message(
                            chat_id=CHANNEL_ID,
                            text=message,
                            parse_mode="HTML"
                        )
                    except Exception as e:
                        print(f"Error sending message: {e}")

                current_status[i] = returncode

            # Wait 30 seconds before next check
            await asyncio.sleep(30)

        except Exception as e:
            print(f"Error in server_status_periodic: {e}")
            await asyncio.sleep(30)

async def main():
    async with application:
        await application.start()
        await on_ready()
        await application.stop()

if __name__ == "__main__":
    asyncio.run(main())
