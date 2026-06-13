import discord
from discord import app_commands
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

app = Flask('')

@app.route('/')
def home():
    return "CRAKZY BOT 24/7 ONLINE"

@client.event
async def on_ready():
    await tree.sync()
    print(f'✅ CRAKZY BOT en línea como {client.user}')

@tree.command(name="ping", description="Checa el lag")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(client.latency * 1000)}ms 🍅')

def run_bot():
    client.run(TOKEN)

def keep_alive():
    app.run(host='0.0.0.0', port=10000)

Thread(target=keep_alive).start()
run_bot()
