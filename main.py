import os
import discord
from discord.ext import commands
from mcstatus import JavaServer

TOKEN = os.getenv('DISCORD_TOKEN')
MINECRAFT_SERVER_IP = os.getenv('MINECRAFT_SERVER_IP')  # Contoh: 'play.example.com'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!a ", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def status(ctx):
    """Cek status server Minecraft."""
    if not MINECRAFT_SERVER_IP:
        await ctx.send("⚠️ MINECRAFT_SERVER_IP tidak disetel. Tambahkan di Secrets.")
        return
    try:
        server = JavaServer.lookup(MINECRAFT_SERVER_IP)
        status = server.status()
        ping = server.ping()
        players = status.players.sample if status.players.sample is not None else []
        player_names = ", ".join([player.name for player in players]) if players else "None"
        # Handle MOTD
        motd = "None"
        if isinstance(status.description, dict) and 'text' in status.description:
            motd = status.description['text'] or "None"
        elif isinstance(status.description, str):
            motd = status.description
        await ctx.send(
            f"✅ Server Online!\n"
            f"Players: {status.players.online}/{status.players.max}\n"
            f"MOTD: {motd}\n"
            f"Ping: {ping:.2f} ms\n"
            f"Online Players: {player_names}\n"
            f"Version: {status.version.name}"
        )
    except Exception as e:
        await ctx.send(f"⚠️ Error fetching server status: {e}")

bot.run(TOKEN)