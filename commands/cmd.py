import discord
from discord.ext import commands

def setup_general_commands(bot):
    @bot.command(name="ajuda")
    async def ajuda(ctx):
        await ctx.send("""
        ```md
# Todos os comandos da Kalle por categoria:
-----------------------------------

* O prefixo para usar esse bot é o "." todos os comandos abaixo usam essa regra para serem evocados.

## Moderation:
- `kick (user)`: expulsa um usuário do server.
- `ban (user)`: bane um usuário do server.
- `clear (amount)`: função de chat clear ele limpa a quantidade de mensagens que você especificar no amount.
- `ticket`: cria uma thread privada para o usuário que executou o comando.
- `mute (user) (tempo de mute) (reason)`: muta um usuário e adiciona um cargo de mute na pessoa, coleta informações do usuário.
- `unmute (user)`: tira o cargo de mute e o mute do usuário.

## para os comandos de música digite ".mhelp" o bot te enviara uma dm com os comandos.
* Os comandos de música diferente dos comandos normais usam ".m" ao invés do . tradicional!

## Fun:
- `oi`: cumprimenta o bot!
- `r (quantidade)d(tipo do dado)`: exemplo `.r d20` rola um dado de 20 faces, `.r 2d10+6` rola dois dados de 10 faces + 6 de modificador.
""")

    @bot.command(name="ticket")
    async def ticket(ctx):
        thread = await ctx.channel.create_thread(name=f"Ticket-{ctx.author.name}", auto_archive_duration=60)
        await thread.add_user(ctx.author)
        await thread.send(f'Thread de suporte criada para {ctx.author.mention}. Somente você e os administradores podem ver.')

    # Slash Commands
    @bot.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f'Olá {interaction.user.mention}.')

    @bot.tree.command(name="skillissue", description="Marca um usuário que tenha skill issue.")
    async def skill_issue(interaction: discord.Interaction, user: discord.Member):
        await interaction.response.send_message(f'{user.mention} Skill Issue.')

def setup(bot):
    setup_general_commands(bot)