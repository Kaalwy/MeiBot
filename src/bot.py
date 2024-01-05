import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import commands as regular_commands

load_dotenv()

TOKEN = os.getenv('KALLE_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='.', intents = discord.Intents.all())

regular_commands.setup(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(TOKEN)