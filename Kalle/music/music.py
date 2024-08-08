import os
import discord
from discord.ext import commands
import yt_dlp

def setup_music_commands(bot):
    # Fila de músicas
    music_queue = []

    @bot.command(name='join', help='Faz o bot entrar no canal de voz')
    async def join(ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f'Conectado ao canal {channel}')
        else:
            await ctx.send('Você precisa estar em um canal de voz para usar este comando.')

    @bot.command(name='leave', help='Faz o bot sair do canal de voz')
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send('Desconectado do canal de voz')
        else:
            await ctx.send('O bot não está em um canal de voz')

    @bot.command(name='play', aliases=['p'], help='Faz com que o bot toque um arquivo MP3 ou uma URL do YouTube')
    async def play(ctx, *, file_name_or_url: str):
        """Comando para tocar um arquivo MP3 do sistema de arquivos ou um vídeo do YouTube."""
        downloads_directory = 'music/downloads/'
        file_name = os.path.basename(file_name_or_url)  # Pegar apenas o nome do arquivo
        file_path = os.path.join(downloads_directory, file_name)

        if ctx.voice_client is None:
            await ctx.send('Eu preciso estar em um canal de voz para tocar música. Use .join primeiro.')
            return

        # Se o argumento é uma URL do YouTube, faça o download do áudio
        if 'youtube.com' in file_name_or_url or 'youtu.be' in file_name_or_url:
            await ctx.send(f'Baixando áudio de: {file_name_or_url}...')
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(downloads_directory, '%(title)s.%(ext)s'),  # Salva com o título na pasta downloads
                }
                os.makedirs(downloads_directory, exist_ok=True)  # Garante que o diretório exista
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(file_name_or_url, download=True)
                    file_path = os.path.join(downloads_directory, f"{info['title']}.mp3")

                await ctx.send(f'Áudio pronto para tocar: {info["title"]}.mp3')
            except Exception as e:
                await ctx.send(f'Ocorreu um erro ao baixar o áudio: {str(e)}')
                return

        # Verifica se o arquivo existe após o download (ou se ele já estava lá)
        if not os.path.isfile(file_path):
            await ctx.send('Arquivo não encontrado mesmo após o download.')
            return

        # Adiciona a música à fila
        music_queue.append(file_path)

        # Se o bot não estiver tocando música, toca a primeira da fila
        if not ctx.voice_client.is_playing():
            await play_next(ctx)

    async def play_next(ctx):
        """Função auxiliar para tocar a próxima música na fila."""
        if music_queue:
            next_song = music_queue.pop(0)  # Pega a próxima música da fila
            source = discord.FFmpegPCMAudio(next_song)
            ctx.voice_client.play(source, after=lambda e: play_next(ctx))
            await ctx.send(f'Tocando: {os.path.basename(next_song)}')
        else:
            await ctx.send('Não há mais músicas na fila.')

    @bot.command(name='stop', help='Para a música atual')
    async def stop(ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('Música parada')
        else:
            await ctx.send('Não há música tocando no momento')

    @bot.command(name='skip', help='Pula a música atual')
    async def skip(ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # Para a música atual
            await ctx.send('Música pulada')
            await play_next(ctx)  # Chama a função para tocar a próxima música
        else:
            await ctx.send('Não há música tocando no momento')

    @bot.command(name='queue', help='Mostra a fila de músicas')
    async def queue(ctx):
        if music_queue:
            queue_list = '\n'.join(os.path.basename(song) for song in music_queue)
            await ctx.send(f'Fila de músicas:\n{queue_list}')
        else:
            await ctx.send('A fila está vazia.')