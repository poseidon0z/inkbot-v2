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


client = commands.Bot(command_prefix="ink ", intents=intents,
                      allowed_mentions=allowed_mentions, application_id=app_id)


@client.event
async def on_ready():
    print(f"Bot is online on account {client.user} ({client.user.id})")


async def cog_loader() -> None:
    """Loads all the cogs stored in /cogs
    """
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await client.load_extension(f"cogs.{file[:-3]}")


async def main():
    await cog_loader()
    await client.start(token)

asyncio.run(main())
