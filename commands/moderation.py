import discord
from discord.ext import commands
from datetime import datetime
import asyncio

def setup_moderation_commands(bot):
    @bot.command(name="mute", aliases=['mutar'], help="silencia um usuario nos chats e muta ele nas calls do servidor por um tempo determinado\nexemplo: .mute @user 15m fazer bobagem\nuse d=dia, h=hora, m=minuto, s=segundo")
    @commands.has_permissions(kick_members=True)
    async def mute(ctx, member: discord.Member, duration: str, *, reason=None):
        MUTE_CHANNEL_ID = 1158441388296392714
        LOG_CHANNEL_ID = 1250788081032892446

        if ctx.channel.id != MUTE_CHANNEL_ID:
            await ctx.send(f'{ctx.author.mention}, você só pode usar este comando em um canal específico.')
            return

        muted_role = discord.utils.get(ctx.guild.roles, name='kalle-mute')
        if not muted_role:
            muted_role = await ctx.guild.create_role(name='kalle-mute')

            # Define as permissões do cargo
            for channel in ctx.guild.channels:
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                overwrite.speak = False
                
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

        message = (
            f"Advertido por: {ctx.author.mention}\n"
            f"Usuário punido: {member.mention}\n"
            f"Nome escrito: {member.name}\n"
            f"ID: {member.id}\n"
            f"Tempo de mute: {duration}\n"
            f"Data: {datetime.now().strftime('%d/%m/%y %H:%M:%S')}\n"
            f"Motivo: {reason if reason else 'Não especificado'}"
        )

        if reason:
            await ctx.send(f'{member.mention} foi mutado com sucesso. Motivo: {reason}')
        else:
            await ctx.send(f'{member.mention} foi mutado com sucesso.')

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(message)

        try:
            await ctx.author.send(f"Você mutou {member.mention} no servidor {ctx.guild.name} (ID: {ctx.guild.id}).\n"
                                  f"O usuário mutado não pode enviar mensagens nos chats e falar nas chamadas de voz.")
        except discord.Forbidden:
            await ctx.send("Não foi possível enviar uma mensagem direta para você, pois você desativou suas mensagens diretas.")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao tentar enviar uma mensagem direta para você: {e}")

        await asyncio.sleep(mute_seconds)
        await member.remove_roles(muted_role)

        try:
            await member.send(f"Seu mute no servidor {ctx.guild.name} acabou.")
        except discord.Forbidden:
            pass

    @bot.command(name="unmute", aliases=['desmutar'], help="desmuta um usuario\n.unmute @user")
    @commands.has_permissions(kick_members=True)
    async def unmute(ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name='kalle-mute')
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} foi desmutado.')
        else:
            await ctx.send(f'{member.mention} não está mutado.')

    @bot.command(name='ban', aliases=['banir'], help="bane um usuario mencionado\nexemplo: .ban @user (reason)")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} foi banido por {ctx.author} pelo seguinte motivo: {reason}')

    @bot.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} foi expulso por {ctx.author} pelo seguinte motivo: {reason}')

    # Em caso de erro de permissao avise ao usuario
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