import discord
from discord.ext import commands
import random
import json
import os
from datetime import datetime

CONFIG_FILE = "greet_config.json"

def load_greet_channel():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file).get("greet_channel")
    return None

def save_greet_channel(channel_id):
    with open(CONFIG_FILE, "w") as file:
        json.dump({"greet_channel": channel_id}, file)

gifs = [
    "https://i.pinimg.com/originals/a0/90/c5/a090c5e7fc684e9fedaeab12869ff0c6.gif",
    "https://i.pinimg.com/originals/a8/bc/29/a8bc29ddeb018d9d32b488dcb6a1092f.gif",
    "https://i.pinimg.com/originals/8c/a3/9d/8ca39d6e212b131dee8d1ead530e9527.gif",
    "https://i.pinimg.com/originals/f5/f2/74/f5f27448c036af645c27467c789ad759.gif",
    "https://i.pinimg.com/originals/2f/43/76/2f437614d7fa7239696a8b34d5e41769.gif"
]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

def setup_general_commands(bot):
    async def send_help_message(ctx_or_interaction):
        help_message = """
        ```md
# Todos os comandos da Mei por categoria:
-----------------------------------

* O prefixo para usar esse bot é o "." todos os comandos abaixo usam essa regra para serem evocados.

## Moderation:
- `kick (user) (reason)`: expulsa um usuário do server.
- `ban (user) (reason)`: bane um usuário do server.
- `clear (amount)`: função de chat clear ele limpa a quantidade de mensagens que você especificar no amount.
- `ticket`: cria uma thread privada para o usuário que executou o comando.
- `mute (user) (tempo de mute) (reason)`: muta um usuário e adiciona um cargo de mute na pessoa, coleta informações do usuário.
- `unmute (user)`: tira o cargo de mute e o mute do usuário.

## Music and call commands (BETA):
- `join`: entra no seu canal de voz.
- `leave`: sai do canal de voz.
- `play (link)`: toca uma musica.
- `skip`: skipa uma musica e toca a proxima na queue.
- `stop`: para todas as musicas da lista.
- `queue`: mostra a lista de musicas a serem tocadas.

## Fun:
- `oi`: cumprimenta o bot!
- `r (quantidade)d(tipo do dado)`: exemplo `.r d20` rola um dado de 20 faces, `.r 2d10+6` rola dois dados de 10 faces + 6 de modificador.
        ```
        """
        if isinstance(ctx_or_interaction, commands.Context):
            await ctx_or_interaction.send(help_message)
        elif isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(help_message)
        elif isinstance(ctx_or_interaction, discord.TextChannel):
            await ctx_or_interaction.send(help_message)

    @bot.command(name="ajuda")
    async def ajuda(ctx):
        await send_help_message(ctx)

    @bot.tree.command(name="ajuda", description="Mostra todos os comandos disponíveis.")
    async def ajuda_slash(interaction: discord.Interaction):
        await send_help_message(interaction)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # Verifica se a mensagem contém apenas a menção ao bot
        if len(message.mentions) == 1 and message.mentions[0] == bot.user and message.content.strip() == f"<@{bot.user.id}>":
            await message.add_reaction('❓')
            await send_help_message(message.channel)
        
        await bot.process_commands(message)

    @bot.command(name="oi", aliases=["olá", "ola", "hello", "hi"])
    async def hello(ctx):
        current_hour = datetime.now().hour

        if 6 <= current_hour < 12:
            greeting = "Bom dia"
        elif 12 <= current_hour < 18:
            greeting = "Boa tarde"
        else:
            greeting = "Boa noite"
        
        await ctx.send(f"{greeting}, {ctx.author.mention}.")

    @bot.command(name="oii", aliases=["hii", "hewwo", "hew", "heya", "oiiee", "oie", "oiie"])
    async def hello(ctx):
        current_hour = datetime.now().hour

        if 0 <= current_hour < 12:
            greetings = ["https://tenor.com/view/wisteriahacks-stelle-good-morning-hsr-honkai-star-rail-gif-7894856137701322105", "https://tenor.com/view/falin-touden-falin-falin-dunmeshi-falin-dungeon-meshi-falin-delicious-in-dungeon-gif-13321700084531761987", "https://tenor.com/view/stelle-hsr-honkai-star-rail-good-morning-picmix-gif-14971906056087973106", "https://tenor.com/view/kafka-honkai-project-sekai-vocaloid-alex-gif-8757130874960721563", "https://tenor.com/view/ado-ado-gif-ado-singer-ado-good-morning-good-morning-gif-5400724748085991472", "https://tenor.com/view/marcille-dunmeshi-marcille-dungeon-meshi-marcille-delicious-in-dungeon-marcille-delicious-in-dungeon-picmix-gif-1241109772456880915", "https://tenor.com/view/ado-readymade-merry-readymade-goodmorning-ado-utaite-gif-15086115743040454412", "https://tenor.com/view/good-morning-good-morning-gif-blue-miku-hatsune-miku-gif-986122290921543599", "https://tenor.com/view/dungeon-meshi-delicious-in-dungeon-good-morning-good-morning-gif-marcille-gif-1782209361987178446", "https://tenor.com/view/good-morning-phoenix-wright-gif-6282626786686229982"]
        elif 12 <= current_hour < 18:
            greetings = ["https://tenor.com/view/leah-pookie-bear-sanae-kochiya-touhou-gif-5920970219019213138", "https://tenor.com/view/good-afternoon-afternoon-dazai-dazai-osamu-bsd-gif-1103807297647988307"]
        else:
            greetings = ["https://tenor.com/view/ado-giragira-gira-gira-good-night-goodnight-gif-5423733055869444136", "https://tenor.com/view/mithrun-dungeon-meshi-dunmeshi-good-night-goodnight-gif-13050234819842792359", "https://tenor.com/view/rei-ayanami-rei-ayanami-evangelion-nge-gif-11364400796140035367", "https://tenor.com/view/dungeon-meshi-delicious-in-dungeon-dungeon-meshi-picmix-dungeon-meshi-goodnight-good-night-images-gif-2661338799817113031", "https://tenor.com/view/furina-goodnight-furina-genshin-genshin-impact-furina-good-night-gif-7110255517157230256"]
        
        greeting = random.choice(greetings)

        await ctx.send(greeting)

    @bot.command(name="ticket")
    async def ticket(ctx):
        thread = await ctx.channel.create_thread(name=f"Ticket-{ctx.author.name}", auto_archive_duration=60)
        await thread.add_user(ctx.author)
        await thread.send(f'Thread de suporte criada para {ctx.author.mention}. Somente você e os administradores podem ver.')

    @bot.command(name="clear", help="Limpa uma quantidade específica de mensagens.")
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int):
        if amount <= 0:
            await ctx.send("Por favor, especifique um número positivo de mensagens para apagar.")
            return
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"{len(deleted)} mensagens apagadas.", delete_after=5)

    @bot.command(name="greet")
    @commands.has_permissions(administrator=True)
    async def set_greet_channel(ctx):
        save_greet_channel(ctx.channel.id)
        await ctx.send(f"Canal de boas-vindas definido para {ctx.channel.mention}.")

    @bot.event
    async def on_member_join(member):
        greet_channel_id = load_greet_channel()
        
        if greet_channel_id:
            channel = bot.get_channel(greet_channel_id)
            
            if channel:
                selected_gif = random.choice(gifs)
                
                embed = discord.Embed(
                    title="Bem-vindo!",
                    description=f"Olá {member.mention}, seja bem-vindo ao servidor!",
                    color=discord.Color.green()
                )
                embed.set_image(url=selected_gif)
                
                await channel.send(embed=embed)

def setup(bot):
    setup_general_commands(bot)