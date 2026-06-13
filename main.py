import discord
import os
from discord.ext import commands
from threading import Thread
from flask import Flask

# Servidor web fake para que Render no mate el bot
app = Flask('')

@app.route('/')
def home():
    return "CRAKZY-BOT vivo"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Bot de Discord
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ CRAKZY BOT en línea como {bot.user}')

def run_bot():
    bot.run(TOKEN)

# Prende Flask y el bot al mismo tiempo
if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()
