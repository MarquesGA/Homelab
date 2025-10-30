import os
import discord
from discord.ext import commands
from discord import app_commands
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")                  # ← Substitua no .env
JELLYSEERR_URL = os.getenv("JELLYSEERR_URL")                # ← Substitua no .env
JELLYSEERR_API_KEY = os.getenv("JELLYSEERR_API_KEY")        # ← Substitua no .env

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

# Busca filmes/séries no Jellyseerr
def search_jellyseerr(query):
    url = f"{JELLYSEERR_URL}/api/v1/search?query={query}"
    headers = {"X-Api-Key": JELLYSEERR_API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json().get("results", [])
    return []

# Envia requisição de mídia
def send_request(media_type, media_id):
    url = f"{JELLYSEERR_URL}/api/v1/request"
    headers = {"X-Api-Key": JELLYSEERR_API_KEY, "Content-Type": "application/json"}
    payload = {"mediaType": media_type, "mediaId": media_id, "requestType": "default_en"}
    resp = requests.post(url, headers=headers, json=payload)
    return resp.ok

# Comando /search
@tree.command(name="search", description="Search and request a movie or series")
@app_commands.describe(query="Movie or series name")
async def search(interaction: discord.Interaction, query: str):
    await interaction.response.defer(ephemeral=True)
    results = search_jellyseerr(query)

    if not results:
        await interaction.followup.send("No results found.", ephemeral=True)
        return

    selected = results[0]  # Seleciona o primeiro resultado automaticamente
    title = selected.get("title") or selected.get("name") or "Unknown Title"
    success = send_request(selected["mediaType"], selected["id"])

    if success:
        await interaction.channel.send(f"✅ Request sent for **{title}**!")
    else:
        await interaction.channel.send("❌ Failed to send request.")

# Comando /info
@tree.command(name="info", description="Bot usage info")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Use /search para buscar e solicitar filmes/séries do Jellyseerr.",
        ephemeral=True
    )

# Evento on_ready
@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")
    try:
        await tree.sync()
        print("🔄 Slash commands synced")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

bot.run(DISCORD_TOKEN)
