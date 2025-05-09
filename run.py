import discord
import logging
import time
from discord.ext import commands
from datetime import datetime

start_time = time.time()
datetime.now()
current_time = datetime.now().astimezone().strftime("%H:%M")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", mode="a", encoding="utf-8"),
    ],
)

logging.getLogger("discord").setLevel(logging.WARNING)
logger = logging.getLogger("Discord Bot")


class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")
    try:
        synced = await self.tree.sync()
        logger.info(f"Successfully synced {len(synced)} commands!")
    except Exception as e:
        logger.warning(f"Failed to sync commands: {e}")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.author.bot:
            return
        
        if self.user in message.mentions:
          await message.channel.send("Hey there! How can I assist you?")
          
        await self.process_commands(message)

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.presences = True
intents.moderation = True
client = Client(command_prefix="!", intents=intents, help_command=None)

# /avatar command
@client.tree.command(name="avatar", description="Display another user's avatar.")
async def avatar(interaction: discord.Interaction, user: discord.User):
    embed = discord.Embed(
        title="",
        color=discord.Color.dark_gray()
    )
    embed.add_field(name="__User Avatar__", value=f'> {user.mention}', inline=False)
    embed.set_image(url=user.avatar.url)
    embed.set_author(name=f'Requested by {interaction.user.name}', url="", icon_url=interaction.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

BOT_TOKEN = 0000  # save your bot token in here

try:
    client.run(f"{BOT_TOKEN}")
except Exception as e:
    logging.critical(f"Failed to start the bot: {e}")
    exit(1)
