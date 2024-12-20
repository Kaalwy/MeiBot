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
        categories = {
            "⚔️ Moderação": """
            `kick (user) (reason)`: Expulsa um usuário do server.
            `ban (user) (reason)`: Bane um usuário do server.
            `clear (amount)`: Limpa a quantidade especificada de mensagens.
            `ticket`: Cria uma thread privada para o usuário.
            `mute (user) (tempo) (reason)`: Muta um usuário com um cargo de mute.
            `unmute (user)`: Remove o mute do usuário.
            """,
            "🎶 Música e Chamadas (BETA)": """
            `join`: Entra no seu canal de voz.
            `leave`: Sai do canal de voz.
            `play (link)`: Toca uma música a partir de um link.
            `skip`: Skipa para a próxima música na fila.
            `stop`: Para todas as músicas na lista.
            `queue`: Mostra a lista de músicas.
            """,
            "🌀 Diversão": """
            `oi`: O bot te cumprimenta!
            `r (quantidade)d(tipo do dado)`: Rola dados para jogos (ex: `.r d20` ou `.r 2d10+6`).
            """,
            "🍰 RPG - Caketale": """
            `caketale`: Inicia a aventura no mundo do Caketale.
            `status`: Mostra o status do personagem no RPG Caketale.
            """
        }
        
        for category, description in categories.items():
            embed = discord.Embed(
                title=category,
                description=description,
                color=discord.Color.red()
            )
            if isinstance(ctx_or_interaction, commands.Context):
                await ctx_or_interaction.send(embed=embed)
            elif isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(embed=embed)
            elif isinstance(ctx_or_interaction, discord.TextChannel):
                await ctx_or_interaction.send(embed=embed)

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

        embed = discord.Embed(
            title="👋 Cumprimento",
            description=f"{greeting}, {ctx.author.mention}!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @bot.command(name="oii", aliases=["hii", "hewwo", "hew", "heya", "oiiee", "oie", "oiie"])
    async def hello_gif(ctx):
        current_hour = datetime.now().hour

        if 0 <= current_hour < 12:
            greetings = ["https://tenor.com/view/wisteriahacks-stelle-good-morning-hsr-honkai-star-rail-gif-7894856137701322105", "https://tenor.com/view/falin-touden-falin-falin-dunmeshi-falin-dungeon-meshi-falin-delicious-in-dungeon-gif-13321700084531761987"]
        elif 12 <= current_hour < 18:
            greetings = ["https://tenor.com/view/leah-pookie-bear-sanae-kochiya-touhou-gif-5920970219019213138"]
        else:
            greetings = ["https://media1.tenor.com/m/S0T4emekYCgAAAAd/ado-giragira.gif"]

        greeting_gif = random.choice(greetings)
        
        embed = discord.Embed(
            title="👋 Cumprimento",
            description=f"{ctx.author.mention}, aqui vai um cumprimento especial!",
            color=discord.Color.purple()
        )
        embed.set_image(url=greeting_gif)
        
        await ctx.send(embed=embed)

    @bot.command(name="ticket")
    async def ticket(ctx):
        thread = await ctx.channel.create_thread(name=f"Ticket-{ctx.author.name}", auto_archive_duration=60)
        await thread.add_user(ctx.author)
        
        embed = discord.Embed(
            title="🖍 Ticket Criado",
            description=f"Thread de suporte criada para {ctx.author.mention}. Somente você e os administradores podem ver.",
            color=discord.Color.orange()
        )
        
        await thread.send(embed=embed)

    @bot.command(name="clear", help="Limpa uma quantidade específica de mensagens.")
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int):
        if amount <= 0:
            embed = discord.Embed(
                title="Erro",
                description="Por favor, especifique um número positivo de mensagens para apagar.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        deleted = await ctx.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="🧹 Cleaning",
            description=f"{len(deleted)} messages has been deleted.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed, delete_after=5)

    @bot.command(name="greet")
    @commands.has_permissions(administrator=True)
    async def set_greet_channel(ctx):
        save_greet_channel(ctx.channel.id)
        
        embed = discord.Embed(
            title="📢 Canal de Boas-vindas Definido",
            description=f"Canal de boas-vindas definido para {ctx.channel.mention}.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

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

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        REACTION_PROBABILITY = 0.02
        RANDOM_EMOJIS = ['✌️', '👋', '🐱', '❤️', '👀', '💅']

        if random.random() < REACTION_PROBABILITY:
            emoji = random.choice(RANDOM_EMOJIS)
            try:
                await message.add_reaction(emoji)
            except discord.HTTPException:
                print(f"Failed to react with emoji {emoji}.")

        if len(message.mentions) == 1 and message.mentions[0] == bot.user and message.content.strip() == f"<@{bot.user.id}>":
            await message.add_reaction('❓')
            await send_help_message(message.channel)
        
        await bot.process_commands(message)

def setup(bot):
    setup_general_commands(bot)