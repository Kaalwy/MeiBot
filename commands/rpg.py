import discord
from discord.ext import commands
import json
import asyncio
import os

DATA_FILE = "player_data.json"

def load_player_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

def save_player_data(player_data):
    with open(DATA_FILE, "w") as file:
        json.dump(player_data, file, indent=4)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

player_data = load_player_data()

def setup_rpg_commands(bot):
    async def send_intro(ctx):
        intro_text = (
            "Boas vindas a Caketale.\n"
            "Antes de começar nossa jornada, precisamos criar seu personagem com um pequeno quiz que determinará seus atributos.\n"
            "Prepara-te!"
        )
        await asyncio.sleep(0.2)
        await ctx.send(intro_text)

    async def run_quiz(ctx, player_stats, player_skills, chosen_class):
        class_specific_questions = {
            "Guerreiro": [
                {
                    "question": "Você está em desvantagem numérica em um combate contra 3 guerreiros. O que você faz?",
                    "choices": ["Luta até a última gota de sangue", "Foge pela sua vida", "Defende os aliados restantes"],
                    "stats": {"Luta até a última gota de sangue": "força", "Foge pela sua vida": "destreza", "Defende os aliados restantes": "constituição"}
                },
            ],
            "Ladino": [
                {
                    "question": "Desde muito jovem, você tinha que escolher entre se tornar um batedor de carteira, um destravador de portas ou tentar lutar e levar uma vida honesta.",
                    "choices": ["Torne-se um batedor de carteiras", "tornar-se um destravador de portas", "levar uma vida honesta"],
                    "stats": {"Torne-se um batedor de carteiras": "destreza", "tornar-se um destravador de portas": "inteligência", "levar uma vida honesta": "sabedoria"}
                },
                {
                    "question": "Você poderia ter simplesmente abandonado seus companheiros e mantido sua vida, ou poderia ter lutado até o último suspiro. Mas o que você fará?",
                    "choices": ["abandonadar companheiros", "Lutar até o último suspiro."],
                    "skills": {"abandonadar companheiros": "plano de fuga", "Lutar até o último suspiro.": "sede de sangue"}
                },
            ],
            "Mago": [
                {
                    "question": "Durante uma missão, você encontra um antigo livro de feitiços. O que você faz?",
                    "choices": ["Tenta decifrar as páginas e aprender", "Usa o livro para trocar por recursos", "Deixa o livro para trás"],
                    "stats": {"Tenta decifrar as páginas e aprender": "sabedoria", "Usa o livro para trocar por recursos": "carisma", "Deixa o livro para trás": "constituição"}
                },
                {
                    "question": "Durante uma batalha, você percebe que um feitiço poderoso pode te salvar. O que você faz?",
                    "choices": ["Usa o feitiço imediatamente", "Espera o momento certo", "Evita usá-lo para poupar energia"],
                    "skills": {"Usa o feitiço imediatamente": "explosão arcana", "Espera o momento certo": "concentração arcana", "Evita usá-lo para poupar energia": "disciplina mágica"}
                },
            ],
            "Clérigo": [
                {
                    "question": "Você descobre que um dos seus aliados esconde um segredo perigoso. Como você lida com isso?",
                    "choices": ["Confronto-o imediatamente", "Investigo mais antes de tomar uma decisão", "Ignoro e continuo a missão"],
                    "stats": {"Confronto-o imediatamente": "força", "Investigo mais antes de tomar uma decisão": "inteligência", "Ignoro e continuo a missão": "sabedoria"}
                },
            ],
            "Bardo": [
                {
                    "question": "Você tem a oportunidade de fazer uma nova amizade. O que você faz?",
                    "choices": ["Faço amizade imediatamente", "Avalio se vale a pena", "Evito novas amizades por enquanto"],
                    "stats": {"Faço amizade imediatamente": "carisma", "Avalio se vale a pena": "sabedoria", "Evito novas amizades por enquanto": "inteligência"}
                },
            ],
            "Paladino": [
                {
                    "question": "Você se depara com uma escolha difícil entre salvar um amigo ou completar uma missão. O que você faz?",
                    "choices": ["Salvo meu amigo", "Completo a missão", "Tento encontrar uma solução para salvar ambos"],
                    "stats": {"Salvo meu amigo": "constituição", "Completo a missão": "inteligência", "Tento encontrar uma solução para salvar ambos": "carisma"}
                },
            ],
        }
        
        questions = class_specific_questions.get(chosen_class, [])
        
        for question in questions:
            question_text = f"{question['question']}\n" + "\n".join([f"{i+1}. {choice}" for i, choice in enumerate(question["choices"])])
            await ctx.send(question_text)

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

            try:
                response = await bot.wait_for("message", check=check, timeout=120.0)
                choice_index = int(response.content) - 1

                if choice_index in range(len(question["choices"])):
                    chosen_stat_or_skill = question["choices"][choice_index]
                    if "stats" in question:
                        stat_affected = question["stats"][chosen_stat_or_skill]
                        player_stats[stat_affected] += 1
                        await ctx.send(f"*isso aumenta **{stat_affected}***")
                    elif "skills" in question:
                        skill_learned = question["skills"][chosen_stat_or_skill]
                        player_skills.append(skill_learned)
                        await ctx.send(f"*Você aprendeu uma nova habilidade: **{skill_learned}***")
                else:
                    await ctx.send("Escolha inválida.")
            except:
                await ctx.send("Tempo esgotado!")

    async def choose_class(ctx):
        class_options = ["1. Guerreiro", "2. Ladino", "3. Mago", "4. Clérigo", "5. Bardo", "6. Paladino"]
        await ctx.send("Escolha a classe do seu personagem:\n" + "\n".join(class_options))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

        try:
            response = await bot.wait_for("message", check=check, timeout=30.0)
            choice = int(response.content)

            class_mapping = {
                1: "Guerreiro",
                2: "Ladino",
                3: "Mago",
                4: "Clérigo",
                5: "Bardo",
                6: "Paladino"
            }
            
            if choice in class_mapping:
                chosen_class = class_mapping[choice]
                await ctx.send(f"Você escolheu: {chosen_class}.")
                return chosen_class
            else:
                await ctx.send("Escolha inválida.")
                return await choose_class(ctx)
        except:
            await ctx.send("Tempo esgotado!")
            return None

    async def choose_gender(ctx):
        gender_options = ["1. Masculino", "2. Feminino", "3. Outro"]
        await ctx.send("Agora, escolha o gênero do seu personagem:\n" + "\n".join(gender_options))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

        try:
            response = await bot.wait_for("message", check=check, timeout=30.0)
            choice = int(response.content)

            if choice == 1:
                await ctx.send("Você escolheu: Masculino.")
            elif choice == 2:
                await ctx.send("Você escolheu: Feminino.")
            elif choice == 3:
                await ctx.send("Você escolheu: Outro.")
            else:
                await ctx.send("Escolha inválida.")
        except:
            await ctx.send("Tempo esgotado!")

    @bot.command(name="caketale")
    async def start(ctx):
        await send_intro(ctx)

        await ctx.send("Qual será o nome do seu personagem?")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            response = await bot.wait_for('message', check=check, timeout=60.0)
            character_name = response.content
        except asyncio.TimeoutError:
            await ctx.send("Você demorou muito para responder. Tente novamente.")
            return

        player_stats = {"força": 1, "destreza": 1, "constituição": 1, "inteligência": 1, "sabedoria": 1, "carisma": 1}
        player_skills = []
        
        chosen_class = await choose_class(ctx)
        if not chosen_class:
            return

        await choose_gender(ctx)

        await run_quiz(ctx, player_stats, player_skills, chosen_class)

        player_name = str(ctx.author)
        player_data[player_name] = {
            "nome_personagem": character_name,
            "classe": chosen_class,
            "atributos": player_stats,
            "habilidades": player_skills
        }
        save_player_data(player_data)

        await ctx.send(f"Personagem salvo com sucesso! Bem-vindo à aventura, **{character_name}**.")

    @bot.command(name="status")
    async def status(ctx):
        player_name = str(ctx.author)
        
        if player_name in player_data:
            character = player_data[player_name]
            status_message = (
                f"## **Nome**: {character['nome_personagem']}\n"
                f"### **Classe**: {character['classe']}\n"
                f"**Status**\n" +
                "\n".join([f"**{stat.capitalize()}**: {value}" for stat, value in character['atributos'].items()]) +
                "\n**Habilidades**\n" +
                "\n".join([f"- {skill}" for skill in character['habilidades']])
            )
            await ctx.send(status_message)
        else:
            await ctx.send("Você não tem um personagem criado. Use o comando .caketale para começar.")

setup_rpg_commands(bot)