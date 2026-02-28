import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import itertools

# Load environment variables
load_dotenv()

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# -----------------------------
# ROTATING STATUS (every 5 sec)
# -----------------------------
statuses = itertools.cycle([
    "UNBLOCKING",
    "LOL...",
    "RIP filters",
    "GGUI OS"
])

@tasks.loop(seconds=5)
async def rotate_status():
    await bot.change_presence(activity=discord.Game(next(statuses)))

# -----------------------------
# BOT READY
# -----------------------------
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    rotate_status.start()

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# -----------------------------
# /ping
# -----------------------------
@bot.hybrid_command(name="ping", description="Replies with pong")
async def ping(ctx):
    await ctx.send('pong')

# -----------------------------
# /hello
# -----------------------------
@bot.hybrid_command(name="hello", description="Says hello to the user")
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}! 😃")

# -----------------------------
# /announce
# -----------------------------
@bot.tree.command(name="announce", description="Send a neon announcement")
async def announce(interaction: discord.Interaction, message: str):
    embed = discord.Embed(
        title="📢 Announcement",
        description=message,
        color=0x00E5FF
    )
    await interaction.response.send_message(embed=embed)

# -----------------------------
# /poll
# -----------------------------
@bot.tree.command(name="poll", description="Create a neon Yes/No poll")
async def poll(interaction: discord.Interaction, question: str):
    embed = discord.Embed(
        title="💠 Neon Poll",
        description=question,
        color=0x00E5FF
    )

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Yes", style=discord.ButtonStyle.primary))
    view.add_item(discord.ui.Button(label="No", style=discord.ButtonStyle.primary))

    await interaction.response.send_message(embed=embed, view=view)

# -----------------------------
# RUN BOT
# -----------------------------
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("No token found. Make sure DISCORD_TOKEN is set in your environment variables.")
    bot.run(token)
