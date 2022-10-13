# This example requires the 'message_content' intent.

import discord
import logging
import os
import logging.handlers

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


def remove_prefix(text):
    return text[:-5]


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello! @{remove_prefix(str(message.author))}')

    elif message.content.startswith('```python') and message.content.endswith("```"):
        await message.channel.send(f'```hello world```')

client.run(os.getenv('DISCORD_TOKEN'))
