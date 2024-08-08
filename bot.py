import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import wavelink

load_dotenv()
TOKEN = os.getenv('KALLE_TOKEN')

# define os intents para o bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

#? funcao que cria o prefixo e retorna ele
def get_prefix(bot, message):
    prefixes = ['.', f'<@!{bot.user.id}> ', f'<@{bot.user.id}> ']
    return commands.when_mentioned_or(*prefixes)(bot, message)

#? cria instancia do bot
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    #? sincroniza comandos globais
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f'Error syncing commands: {e}')

#? carrega comandos
from music.music import setup_music_commands
setup_music_commands(bot)

from commands.dice import setup_dice_commands
setup_dice_commands(bot)

from commands.moderation import setup_moderation_commands
setup_moderation_commands(bot)

from commands.cmd import setup_general_commands
setup_general_commands(bot)

bot.run(TOKEN)