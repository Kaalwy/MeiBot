from discord.ext import commands
import asyncio
import discord
import random

def setup(bot):
    @bot.command(name="commands")
    async def show_commands(ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(1)
        await ctx.send("""
# All Kalle Commands by Category:
-----------------------------------

## Moderation:
- `.kick {user}`: Kick a user from the server.
- `.ban {user}`: Ban a user from the server.
- `.timeout {user} {time in seconds}`: Temporarily mute a user for a specified duration.
- `.clear {quantity}`: delete the quantity of messages specify in the channel
- `.ticket:` cria uma thread privada para o usuário que executou o comando.

## Main Voice Commands:
- `.join`: Make the bot join your voice channel.
- `.disconnect`: Make the bot leave the voice channel.
- `.p [link -> soundcloud, youtube]`, alias `.play`: "play music on the currently channel"
- `pause` "pauses the song" -> `.resume` to continue!

### aliases {
  settings = [ status ]

  lyrics = [ letra ]
  nowplaying = [ np, current ]
  play = [ p ]
  playlists = [ pls, pl ]
  queue = [ list, qeue ]
  remove = [ delete, del ]
  scsearch = [ scs ]
  search = [ ytsearch ]
  shuffle = [ shfl ]
  skip = [ voteskip, pular ]

  prefix = [ setprefix ]
  setdj = [ dj ]
  settc = [ tc ]
  setvc = [ vc ]

  forceremove = [ forcedelete, modremove, moddelete ]
  forceskip = [ modskip ]
  movetrack = [ move ]
  pause = []
  playnext = [ pn ]
  repeat = [ rep ]
  skipto = [ jumpto ]
  stop = []
  volume = [ vol ]
}

## Fun:
- `.hello`: Greet the bot!
- `.roll {dice}`: Roll a specified number of dice.

### Usage Examples:
- `.kick @User505`: Kick the user named User505.
- `.ban @User404`: Ban the user named User404.
- `.timeout @User727 69`: Mute User727 for 69 seconds.
- `.join`: Bot joins your voice channel.
- `.disconnect`: Bot leaves the voice channel.
- `.hello`: Bot greets you.
- `.roll 1d20`: Roll one d20 side dice.
        """)

    @bot.command(name="hello")
    async def say_hello(ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(2)
        greetings = ['Hello!', 'Hi there!', 'Hey!', 'What\'s up?']
        await ctx.send(random.choice(greetings))

    @bot.command(name="vote")
    async def vote(ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(0.7)
        await ctx.send("you can vote in Kalle by the link down below:\nhttps://top.gg/bot/1141449029440503858/vote")

    @bot.command(name="clear")
    @commands.has_permissions(manage_channels=True)
    async def clear(ctx, quantity: int):
            await ctx.channel.purge(limit=quantity)

    @bot.command(name="roll", aliases=["rol", "r", "rl", "Roll", "R", "Rl"])
    async def roll_dice(ctx, num_faces: int):
        num_faces = get_num_faces(num_faces)
        result = random.randint(1, num_faces)

        await ctx.send(f"rolled a d{num_faces} and get a {result}!")


    @bot.command(name="ticket")
    @commands.has_permissions(manage_channels=True)
    async def ticket(ctx): 
        thread = await ctx.channel.create_thread(name=f'Ticket for {ctx.author}', auto_archive_duration=60)

        await thread.add_user(ctx.author)

    def get_num_faces(num_faces):
        if num_faces == 0:
            return 1
        elif num_faces % 2 == 0:
            return num_faces
        else:
            return num_faces + 1

    @bot.command(name="timeout")
    @commands.has_permissions(kick_members=True)
    async def timeout(ctx, member: discord.Member, duration: int):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        if not muted_role:
            muted_role = await ctx.guild.create_role(name='Muted')

        await member.add_roles(muted_role)
        await ctx.send(f'{member.mention} has been muted for {duration} seconds.')

        await asyncio.sleep(duration)
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted.')

    @bot.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been banned.')

    @bot.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked.')