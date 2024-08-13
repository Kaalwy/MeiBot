import discord
from discord.ext import commands

def setup_general_commands(bot):
    async def send_help_message(ctx_or_interaction):
        help_message = """
        ```md
# Todos os comandos da Kalle por categoria:
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

        if bot.user.mentioned_in(message) and len(message.content.split()) == 1:
            await message.add_reaction('❓')
            await send_help_message(message.channel)
        
        await bot.process_commands(message)

    @bot.command(name="ticket")
    async def ticket(ctx):
        thread = await ctx.channel.create_thread(name=f"Ticket-{ctx.author.name}", auto_archive_duration=60)
        await thread.add_user(ctx.author)
        await thread.send(f'Thread de suporte criada para {ctx.author.mention}. Somente você e os administradores podem ver.')

    @bot.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f'Olá {interaction.user.mention}.')

def setup(bot):
    setup_general_commands(bot)