import logging.handlers
import os
from subprocess import Popen, PIPE

import discord
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename="discord.log",
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


def remove_prefix(text):
    return text[:-5]


def remove_python_prefix(discord_code):
    discord_code = discord_code.removeprefix("```python\n")
    discord_code = discord_code[:-3]
    return discord_code


def write_python_on_file(code):
    insert_code = ""
    for line_code in code.split("\n"):
        insert_code += f"\t{line_code}\n"
    insert_code = insert_code[:-1]
    first_file = open("discord_message.py", "w")
    first_file.writelines(
        ["import sys\n", "import traceback\n", f"try:\n{insert_code}"]
    )
    second_file = open("error.txt", "r")
    for line in second_file:
        first_file.write("\n")
        first_file.write(line)

    first_file.close()
    second_file.close()


def run_discord_python_code():
    process = Popen(["python", "discord_message.py"], stdout=PIPE)
    (output, err) = process.communicate()
    process.wait()
    return output, err


def remove_prefix_discord_code_output(output):
    output = output.decode("utf-8")
    return output


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("```python") and message.content.endswith(
            "```"
    ):
        discord_code = remove_python_prefix(message.content)
        write_python_on_file(discord_code)
        output, err = run_discord_python_code()
        code = remove_prefix_discord_code_output(output)
        await message.channel.send(f"```\n{code}\n```")


client.run(os.getenv("DISCORD_TOKEN"))
