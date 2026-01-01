import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle)
    print(f"Bot: Logged in & Set to idle")

bot.run(os.getenv('TEST_BOT_TOKEN'))

