import os
import discord
from discord.ext import commands
import yt_dlp
import asyncio
import re

def setup_music_commands(bot):
    # queue para manter o caminho dos arquivos de musica
    music_queue = []
    # modo de repeticao
    repeat_queue = []
    global repeat_mode
    repeat_mode = False
    last_played_song = None

    @bot.command(name='join', help='Faz o bot entrar no canal de voz')
    async def join(ctx):
        # Diretório para salvar downloads
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

    @bot.command(name='play', aliases=['p'], help='Toca um arquivo MP3, WAV, OGG ou uma URL do YouTube')
    async def play(ctx, *, file_name_or_url: str):
        # Diretório para salvar downloads
        downloads_directory = 'music/downloads/'
        await ctx.send('Baixando o áudio...')
        file_name = os.path.basename(file_name_or_url)
        file_path = os.path.join(downloads_directory, file_name)

        # conecta a call pra tocar a musica
        if ctx.voice_client is None:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
                await ctx.send(f'Conectado ao canal {channel}')
            else:
                await ctx.send('Você precisa estar em um canal de voz para usar este comando.')
                return

        # Verifica se é um link do YouTube
        if 'youtube.com' in file_name_or_url or 'youtu.be' in file_name_or_url:
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',  # Padrão para MP3
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(downloads_directory, '%(title)s.%(ext)s'),
                }

                os.makedirs(downloads_directory, exist_ok=True)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(file_name_or_url, download=True)
                    sanitized_title = re.sub(r'[<>:"/\\|?*]', "", info['title'])
                    extension = file_name_or_url.split('.')[-1]
                    if extension == 'ogg':
                        file_path = os.path.join(downloads_directory, f"{sanitized_title}.ogg")
                    elif extension == 'wav':
                        file_path = os.path.join(downloads_directory, f"{sanitized_title}.wav")
                    else:
                        file_path = os.path.join(downloads_directory, f"{sanitized_title}.mp3")
            except Exception as e:
                await ctx.send(f'Ocorreu um erro ao baixar o áudio: {str(e)}')
                return

        # Verifica se o arquivo foi baixado corretamente
        if not os.path.isfile(file_path):
            await ctx.send('Arquivo não encontrado mesmo após o download.')
            return

        # Adiciona a música à fila
        music_queue.append(file_path)

        # Se não houver música tocando, toca a próxima música na fila
        if not ctx.voice_client.is_playing():
            await play_next(ctx)

    async def play_next(ctx):
        nonlocal last_played_song
        global repeat_mode, repeat_queue

        if ctx.voice_client is None:
            await ctx.send('Erro: o bot não está em um canal de voz.')
            return

        if music_queue or (repeat_mode and repeat_queue):
            # Caso o repeat_mode esteja ativo e a fila esteja vazia, recomeça a fila original
            if not music_queue and repeat_mode and repeat_queue:
                music_queue.extend(repeat_queue)

            next_song = music_queue[0] if music_queue else last_played_song
            source = discord.FFmpegPCMAudio(next_song)
            last_played_song = next_song

            def after_playing(err):
                asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)

            ctx.voice_client.play(source, after=after_playing)
            await ctx.send(f'Tocando: {os.path.basename(next_song)}')

            # Remove a música da fila se o repeat mode estiver desativado
            if not repeat_mode and music_queue:
                music_queue.pop(0)
            else:
                # Se o repeat mode estiver ativado, esvazia a fila mas não exclui a original
                if music_queue:
                    music_queue.pop(0)

            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

            if not repeat_mode:
                try:
                    os.remove(next_song)
                except Exception as e:
                    await ctx.send(f'Erro ao deletar o arquivo: {str(e)}')
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
            ctx.voice_client.stop()
            await ctx.send('Música pulada')
            await play_next(ctx)
        else:
            await ctx.send('Não há música tocando no momento')

    @bot.command(name='queue', help='Mostra a fila de músicas')
    async def queue(ctx):
        if music_queue:
            queue_list = '\n'.join(os.path.basename(song) for song in music_queue)
            await ctx.send(f'Fila de músicas:\n{queue_list}')
        else:
            await ctx.send('A fila está vazia.')

    @bot.command(name='repeat', help='Ativa ou desativa o modo de repetição da fila atual')
    async def repeat(ctx):
        global repeat_mode, repeat_queue
        repeat_mode = not repeat_mode
        if repeat_mode:
            # Salva uma cópia da fila original para repetir
            repeat_queue = music_queue.copy()
            await ctx.send('Modo de repetição ativado. A fila inteira será repetida após todas as músicas.')
        else:
            repeat_queue = []
            await ctx.send('Modo de repetição desativado.')