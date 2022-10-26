import discord
from discord.ext import commands

from pathlib import Path
from json import load

import pymongo

with Path("info.json").open() as f:
    info = load(f)
client_code = info['mongo_client']
mongo_client = pymongo.MongoClient(client_code)
ban_location = mongo_client['bot_data']['banned_users']


def not_banned_cmd():
    def not_banned_cmd_predicate(ctx) -> bool:
        banned_search = ban_location.find_one({"user_id": ctx.author.id})
        if banned_search is None:
            return True
        else:
            return False
    return commands.check(not_banned_cmd_predicate)


def not_banned_slash():
    def not_banned_slash_predicate(interaction: discord.Interaction) -> bool:
        banned_search = ban_location.find_one({"user_id": interaction.user.id})
        if banned_search is None:
            return True
        else:
            return False

    return discord.app_commands.check(not_banned_slash_predicate)
