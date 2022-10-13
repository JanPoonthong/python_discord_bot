import discord
import logging
import os
import logging.handlers

from subprocess import Popen, PIPE
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
    discord_code = discord_code.removeprefix("```python")
    discord_code = discord_code[:-3]
    return discord_code


def write_python_on_file(code):
    with open("discord_message.py", "w") as f:
        # f.writelines(["try:\n", f"\t{code}", "except BaseException as ex:\n", "ex_type, ex_value, ex_traceback = sys.exc_info()\n", "trace_back = traceback.extract_tb(ex_traceback)\n", "stack_trace = list()\n", "for trace in trace_back:\n", "stack_trace.append('File : %s , Line : %d, Func.Name : %s, Message : %s' % (trace[0], trace[1], trace[2], trace[3]))\n, "print('Exception type : %s ' % ex_type.__name__)"
        f.write(f"{code}")


def run_discord_python_code():
    process = Popen(["python", "discord_message.py"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    return output, err


def remove_prefix_discord_code_output(output):
    output = output.decode("utf-8")
    return output


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send(
            f"Hello! @{remove_prefix(str(message.author))}"
        )

    elif message.content.startswith("```python") and message.content.endswith(
        "```"
    ):
        discord_code = remove_python_prefix(message.content)
        write_python_on_file(discord_code)
        output, err = run_discord_python_code()
        code = remove_prefix_discord_code_output(output)
        await message.channel.send(f"```\n{code}\n```")


client.run(os.getenv("DISCORD_TOKEN"))
