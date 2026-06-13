import discord
from discord import app_commands
import requests
import os
import random
import asyncio
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import yt_dlp
from flask import Flask
from threading import Thread

# ==================== KEEP ALIVE PARA RENDER ====================
app = Flask('')
@app.route('/')
def home():
    return "CRAKZY BOT vivo"
Thread(target=lambda: app.run(host='0.0.0.0',port=10000)).start()
# ================================================================

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

TOKEN = os.getenv("DISCORD_TOKEN")

# ==================== EVENTOS ====================
@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Game(name="/help | CRAKZY BOT"))
    print(f'✅ CRAKZY BOT en línea como {client.user}')
    print(f'🚫 Bypass eliminado. 100% legal.')

# ==================== COMANDOS DIVERTIDOS ====================
@tree.command(name="ping", description="Muestra la latencia del bot")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", description=f"Latencia: `{latency}ms`", color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@tree.command(name="8ball", description="Pregúntale a la bola 8 mágica")
@app_commands.describe(pregunta="¿Qué quieres preguntar?")
async def eightball(interaction: discord.Interaction, pregunta: str):
    respuestas = [
        "Sí, definitivamente.", "Es cierto.", "Sin duda.", "Sí.",
        "Puedes contar con ello.", "Probablemente.", "Sí, en mi opinión.",
        "Pregunta de nuevo más tarde.", "Mejor no decirte ahora.",
        "No puedo predecirlo ahora.", "Concéntrate y pregunta otra vez.",
        "No cuentes con ello.", "Mi respuesta es no.", "Mis fuentes dicen que no.",
        "Muy dudoso.", "No.", "JAJA no.", "CRAKZY dice que sí.", "Ni de broma."
    ]
    embed = discord.Embed(title="🎱 Bola 8 Mágica CRAKZY", color=0x9b59b6)
    embed.add_field(name="Pregunta", value=pregunta, inline=False)
    embed.add_field(name="Respuesta", value=random.choice(respuestas), inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="rps", description="Juega Piedra, Papel o Tijera")
@app_commands.choices(choice=[
    app_commands.Choice(name="Piedra 🪨", value="piedra"),
    app_commands.Choice(name="Papel 📄", value="papel"),
    app_commands.Choice(name="Tijera ✂️", value="tijera")
])
async def rps(interaction: discord.Interaction, choice: app_commands.Choice[str]):
    bot_choice = random.choice(["piedra", "papel", "tijera"])
    user_choice = choice.value
    emojis = {"piedra": "🪨", "papel": "📄", "tijera": "✂️"}

    if user_choice == bot_choice:
        result = "🤝 ¡Empate!"
    elif (user_choice == "piedra" and bot_choice == "tijera") or \
         (user_choice == "papel" and bot_choice == "piedra") or \
         (user_choice == "tijera" and bot_choice == "papel"):
        result = "🎉 ¡Ganaste!"
    else:
        result = "😔 Perdiste"

    embed = discord.Embed(title="Piedra, Papel o Tijera", color=0x3498db)
    embed.add_field(name="Tú", value=f"{emojis[user_choice]} {user_choice.capitalize()}", inline=True)
    embed.add_field(name="CRAKZY BOT", value=f"{emojis[bot_choice]} {bot_choice.capitalize()}", inline=True)
    embed.add_field(name="Resultado", value=result, inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="dado", description="Lanza un dado")
@app_commands.describe(caras="Número de caras, default 6")
async def dado(interaction: discord.Interaction, caras: int = 6):
    if caras < 2 or caras > 100:
        await interaction.response.send_message("❌ El dado debe tener entre 2 y 100 caras", ephemeral=True)
        return
    numero = random.randint(1, caras)
    await interaction.response.send_message(f"🎲 Lanzaste un dado de {caras} caras y salió: **{numero}**")

@tree.command(name="meme", description="Meme random de Reddit")
async def meme(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        r = requests.get("https://meme-api.com/gimme", timeout=10).json()
        embed = discord.Embed(title=r['title'], url=r['postLink'], color=0xe67e22)
        embed.set_image(url=r['url'])
        embed.set_footer(text=f"r/{r['subreddit']} | 👍 {r['ups']}")
        await interaction.followup.send(embed=embed)
    except:
        await interaction.followup.send("❌ No pude cargar un meme. Reddit anda CRAKZY.")

@tree.command(name="chiste", description="Te cuento un chiste malo")
async def chiste(interaction: discord.Interaction):
    chistes = [
        "¿Qué le dice un jaguar a otro? Jaguar you? 😂",
        "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
        "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
        "¿Cómo se despiden los químicos? Ácido un placer.",
        "¿Qué le dice una impresora a otra? Esa hoja es tuya o es impresión mía.",
        "¿Por qué CRAKZY BOT no juega al escondite? Porque siempre lo encuentran online."
    ]
    await interaction.response.send_message(random.choice(chistes))

# ==================== COMANDOS ÚTILES ====================
@tree.command(name="traducir", description="Traduce texto a cualquier idioma")
@app_commands.describe(texto="Texto a traducir", idioma="Código: es, en, ja, fr, de. Default: es")
async def traducir(interaction: discord.Interaction, texto: str, idioma: str = "es"):
    await interaction.response.defer()
    try:
        resultado = GoogleTranslator(source='auto', target=idioma).translate(texto)
        embed = discord.Embed(title="🌐 Traductor CRAKZY", color=0x1abc9c)
        embed.add_field(name="Original", value=texto[:1024], inline=False)
        embed.add_field(name=f"Traducido [{idioma}]", value=resultado[:1024], inline=False)
        await interaction.followup.send(embed=embed)
    except:
        await interaction.followup.send("❌ Error. Usa códigos como: `en`, `es`, `ja`, `fr`, `de`")

@tree.command(name="clima", description="Muestra el clima de una ciudad")
@app_commands.describe(ciudad="Ejemplo: Querétaro, Tokyo, Madrid")
async def clima(interaction: discord.Interaction, ciudad: str):
    await interaction.response.defer()
    try:
        r = requests.get(f"http://wttr.in/{ciudad}?format=j1", timeout=10).json()
        current = r['current_condition'][0]
        temp = current['temp_C']
        desc = current['weatherDesc'][0]['value']
        humedad = current['humidity']

        embed = discord.Embed(title=f"🌤️ Clima en {ciudad.title()}", color=0x3498db)
        embed.add_field(name="Temperatura", value=f"{temp}°C", inline=True)
        embed.add_field(name="Estado", value=desc, inline=True)
        embed.add_field(name="Humedad", value=f"{humedad}%", inline=True)
        await interaction.followup.send(embed=embed)
    except:
        await interaction.followup.send("❌ No encontré esa ciudad. Escríbela bien.")

@tree.command(name="avatar", description="Muestra el avatar de un usuario")
@app_commands.describe(member="Usuario, si no pones nada sale el tuyo")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"Avatar de {member.display_name}", color=member.color)
    embed.set_image(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name="encuesta", description="Crea una encuesta rápida")
@app_commands.describe(pregunta="¿Qué quieres preguntar?")
async def encuesta(interaction: discord.Interaction, pregunta: str):
    embed = discord.Embed(title="📊 Encuesta CRAKZY", description=pregunta, color=0xf1c40f)
    embed.set_footer(text=f"Encuesta de {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@tree.command(name="recordatorio", description="Te mando un recordatorio en X minutos")
@app_commands.describe(minutos="En cuántos minutos", mensaje="Qué te recuerdo")
async def recordatorio(interaction: discord.Interaction, minutos: int, mensaje: str):
    if minutos > 1440:
        await interaction.response.send_message("❌ Máximo 1440 minutos = 24 horas", ephemeral=True)
        return

    await interaction.response.send_message(f"⏰ Ok, te recuerdo `{mensaje}` en {minutos} minutos", ephemeral=True)
    await asyncio.sleep(minutos * 60)
    try:
        await interaction.user.send(f"⏰ **Recordatorio CRAKZY:** {mensaje}")
    except:
        await interaction.channel.send(f"{interaction.user.mention} ⏰ **Recordatorio:** {mensaje}")

# ==================== MÚSICA ====================
@tree.command(name="play", description="Reproduce música de YouTube")
@app_commands.describe(busqueda="Nombre de la canción o link de YouTube")
async def play(interaction: discord.Interaction, busqueda: str):
    if not interaction.user.voice:
        await interaction.response.send_message("❌ Métete a un canal de voz primero", ephemeral=True)
        return

    await interaction.response.defer()
    voice_channel = interaction.user.voice.channel

    try:
        voice_client = interaction.guild.voice_client
        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_client.channel!= voice_channel:
            await voice_client.move_to(voice_channel)
    except:
        await interaction.followup.send("❌ No me pude conectar al canal de voz")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'source_address': '0.0.0.0'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(busqueda, download=False)
            if 'entries' in info:
                info = info['entries'][0]
        except:
            await interaction.followup.send("❌ No encontré esa canción")
            return

    url = info['url']
    titulo = info['title']

    voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice_client.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))

    embed = discord.Embed(title="🎵 Reproduciendo ahora", description=f"[{titulo}]({info['webpage_url']})", color=0x2ecc71)
    embed.set_thumbnail(url=info.get('thumbnail'))
    embed.set_footer(text="CRAKZY BOT DJ")
    await interaction.followup.send(embed=embed)

@tree.command(name="stop", description="Para la música y me desconecto")
async def stop(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("⏹️ Música detenida. Me salí del canal.")
    else:
        await interaction.response.send_message("❌ No estoy en ningún canal de voz", ephemeral=True)

# ==================== HELP ====================
@tree.command(name="help", description="Lista todos los comandos")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🤖 Comandos de CRAKZY BOT", description="Aquí tienes todo lo que puedo hacer:", color=0x7289db)
    embed.add_field(name="🎮 Diversión", value="`/8ball` `/rps` `/dado` `/meme` `/chiste`", inline=False)
    embed.add_field(name="🛠️ Útiles", value="`/traducir` `/clima` `/avatar` `/encuesta` `/recordatorio`", inline=False)
    embed.add_field(name="🎵 Música", value="`/play` `/stop` - Únete a un canal de voz primero", inline=False)
    embed.add_field(name="📊 Info", value="`/ping` `/help`", inline=False)
    embed.set_footer(text="CRAKZY BOT v2.0 - Sin bypass, 100% legal 😎")
    await interaction.response.send_message(embed=embed)

# ==================== EJECUCIÓN ====================
if __name__ == "__main__":
    if TOKEN:
        client.run(TOKEN)
    else:
        print("❌ Falta DISCORD_TOKEN en Environment Variables de Render")
