import discord
from discord.ext import commands
from datetime import datetime
import asyncio

def setup_moderation_commands(bot):
    MUTE_CHANNEL_ID = 111111111111111111
    LOG_CHANNEL_ID = 111111111111111111
    EMBED_COLOR = 0x5c8dd6

    async def send_log_embed(ctx, action, member, duration=None, reason=None):
        embed = discord.Embed(
            title=f"{action.capitalize()} - Registro",
            color=EMBED_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Autor da Ação", value=ctx.author.mention, inline=False)
        embed.add_field(name="Usuário", value=member.mention, inline=False)
        embed.add_field(name="Nick", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        if duration:
            embed.add_field(name="Duração", value=duration, inline=True)
        embed.add_field(name="Motivo", value=reason if reason else "Não especificado", inline=False)
        embed.set_footer(text=f"Ação executada em {ctx.guild.name}")

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

    @bot.command(name="mute", aliases=['mutar'], help="Silencia um usuário nos chats e muta ele nas calls do servidor por um tempo determinado.")
    @commands.has_permissions(kick_members=True)
    async def mute(ctx, member: discord.Member, duration: str, *, reason=None):
        if ctx.channel.id != MUTE_CHANNEL_ID:
            await ctx.send(f'{ctx.author.mention}, você só pode usar este comando em um canal específico.')
            return

        muted_role = discord.utils.get(ctx.guild.roles, name='kalle-mute')
        if not muted_role:
            muted_role = await ctx.guild.create_role(name='kalle-mute')
            for channel in ctx.guild.channels:
                overwrite = discord.PermissionOverwrite(send_messages=False, speak=False)
                await channel.set_permissions(muted_role, overwrite=overwrite)

        await member.add_roles(muted_role)

        time_multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        time_unit = duration[-1]
        if time_unit not in time_multiplier:
            await ctx.send("Formato de duração inválido. Use 's' para segundos, 'm' para minutos, 'h' para horas, ou 'd' para dias.")
            await member.remove_roles(muted_role)
            return

        try:
            time_amount = int(duration[:-1])
            mute_seconds = time_amount * time_multiplier[time_unit]
        except ValueError:
            await ctx.send("Formato de duração inválido. Use um número seguido por 's', 'm', 'h', ou 'd'.")
            await member.remove_roles(muted_role)
            return

        await ctx.send(f'{member.mention} foi mutado com sucesso. Motivo: {reason if reason else "Não especificado"}')

        await send_log_embed(ctx, "mute", member, duration, reason)

        await asyncio.sleep(mute_seconds)
        await member.remove_roles(muted_role)

        try:
            await member.send(f"Seu mute no servidor {ctx.guild.name} acabou.")
        except discord.Forbidden:
            pass

    @bot.command(name="unmute", aliases=['desmutar'], help="Desmuta um usuário.")
    @commands.has_permissions(kick_members=True)
    async def unmute(ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name='kalle-mute')
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} foi desmutado.')
        else:
            await ctx.send(f'{member.mention} não está mutado.')

        await send_log_embed(ctx, "unmute", member)

    @bot.command(name='ban', aliases=['banir'], help="Bane um usuário mencionado.")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        if ctx.channel.id != MUTE_CHANNEL_ID:
            await ctx.send(f'{ctx.author.mention}, você só pode usar este comando em um canal específico.')
            return

        await member.ban(reason=reason)
        await ctx.send(f'{member} foi banido por {ctx.author} pelo seguinte motivo: {reason}')

        await send_log_embed(ctx, "banimento", member, reason=reason)

    @bot.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        if ctx.channel.id != MUTE_CHANNEL_ID:
            await ctx.send(f'{ctx.author.mention}, você só pode usar este comando em um canal específico.')
            return

        await member.kick(reason=reason)
        await ctx.send(f'{member} foi expulso por {ctx.author} pelo seguinte motivo: {reason}')

        await send_log_embed(ctx, "expulsão", member, reason=reason)

    @mute.error
    @unmute.error
    @ban.error
    @kick.error
    async def error_handler(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Você não tem permissão para usar este comando.')
        else:
            await ctx.send('Ocorreu um erro. Tente novamente.')

def setup(bot):
    setup_moderation_commands(bot)