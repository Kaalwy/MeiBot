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
    repeat_mode = False

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

    @bot.command(name='play', aliases=['p'], help='Toca um arquivo MP3 ou uma URL do YouTube')
    async def play(ctx, *, file_name_or_url: str):
        # Diretório para salvar downloads
        downloads_directory = 'music/downloads/'
        file_name = os.path.basename(file_name_or_url)
        file_path = os.path.join(downloads_directory, file_name)

        # conecta a call pra tocar a musica
        if ctx.voice_client is None:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f'Conectado ao canal {channel}')

        # verifica se o link e do youtube
        if 'youtube.com' in file_name_or_url or 'youtu.be' in file_name_or_url:
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(downloads_directory, '%(title)s.%(ext)s'),
                }
                os.makedirs(downloads_directory, exist_ok=True)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(file_name_or_url, download=True)
                    # limpa um pouco o titulo na pasta de downloads
                    sanitized_title = re.sub(r'[<>:"/\\|?*]', "", info['title'])
                    file_path = os.path.join(downloads_directory, f"{sanitized_title}.mp3")
            except Exception as e:
                await ctx.send(f'Ocorreu um erro ao baixar o áudio: {str(e)}')
                return

        # verifica se o arquivo foi baixado corretamente
        if not os.path.isfile(file_path):
            await ctx.send('Arquivo não encontrado mesmo após o download.')
            return

        # adiciona a musica a queue
        music_queue.append(file_path)

        # se nao tiver musica tocando...
        if not ctx.voice_client.is_playing():
            await play_next(ctx) # toque a proxima musica da fila

    async def play_next(ctx):
        """Função auxiliar para tocar a próxima música na fila."""
        global repeat_mode

        if music_queue:
            # pega a proxima musica da queue
            next_song = music_queue.pop(0)
            source = discord.FFmpegPCMAudio(next_song)
            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
            await ctx.send(f'Tocando: {os.path.basename(next_song)}')

            # Se o repeat_mode estiver ativado, coloca a música de volta na fila
            if repeat_mode:
                music_queue.append(next_song)

            # espera a musica terminar
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

            # depois de parar se nao estiver no modo repeat remove a musica dos downloads a fim de otimizar espaco
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
            # mostra a queue
            queue_list = '\n'.join(os.path.basename(song) for song in music_queue)
            await ctx.send(f'Fila de músicas:\n{queue_list}')
        else:
            await ctx.send('A fila está vazia.')

    @bot.command(name='repeat', help='Ativa ou desativa o modo de repetição da fila')
    async def repeat(ctx):
        global repeat_mode
        repeat_mode = not repeat_mode
        if repeat_mode:
            await ctx.send('Modo de repetição ativado. A fila inteira será repetida.')
        else:
            await ctx.send('Modo de repetição desativado.')

def setup(bot):
    setup_music_commands(bot)