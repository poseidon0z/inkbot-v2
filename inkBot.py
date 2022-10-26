import asyncio

import discord
from discord.ext import commands

import os
from pathlib import Path
from json import load

# Makes sure bot can't ping everyone or roles accidentally
allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)

# set intents to default, and also add message content so the sync command can be run
intents = discord.Intents.default()
intents.message_content = True

# load token and application id from json
with Path("info.json").open() as f:
    config = load(f)
token = config["token"]
app_id = config["app_id"]

# removing need for underscores in using jsk
os.environ['JISHAKU_NO_UNDERSCORE'] = 'true'

# make traceback appear in same channel as sent message
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'

client = commands.Bot(command_prefix="ink2 ", intents=intents,
                      allowed_mentions=allowed_mentions, application_id=app_id)


@client.event
async def on_ready():
    print(f"Bot is online on account {client.user} ({client.user.id})")
    channel = client.get_channel(838425596421079060)
    await channel.send(f"{client.user} ({client.user.id}) is now active!")


async def cog_loader() -> None:
    """Loads all the cogs stored in /cogs
    """
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await client.load_extension(f"cogs.{file[:-3]}")

    await client.load_extension("jishaku")


async def main():
    await cog_loader()
    await client.start(token)

asyncio.run(main())
