import asyncio

import discord
from discord.ext import commands

import os
from pathlib import Path
from json import load
import pymongo

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
client_code = config['mongo_client']
mongo_client = pymongo.MongoClient(client_code)
command_use_location = mongo_client['bot_data']['command_data']

# removing need for underscores in using jsk
os.environ['JISHAKU_NO_UNDERSCORE'] = 'true'

# make traceback appear in same channel as sent message
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'

client = commands.Bot(command_prefix="ink2 ", intents=intents,
                      allowed_mentions=allowed_mentions, application_id=app_id)


@client.after_invoke
async def command_logger(self, ctx) -> None:
    print("test successful")
    command_use_location.update_one({'user': ctx.author.id}, {'$inc': {ctx.command.name: 1}}, upsert=True)


async def cog_loader() -> None:
    """Loads all the cogs stored in /cogs"""
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await client.load_extension(f"cogs.{file[:-3]}")

    await client.load_extension("jishaku")


async def main():
    """Load all cogs and start the bot"""
    await cog_loader()
    await client.start(token)

asyncio.run(main())
