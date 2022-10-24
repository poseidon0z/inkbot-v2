import discord

from pathlib import Path
from json import load


class inkBot(discord.Client):
    r"""Represents the client connection that runs the bot"""
    async def on_ready(self) -> None:
        """Runs code if the bot has successfully started"""
        print(f"{self.user} is online!")


intents = discord.Intents.default()
intents.message_content = True

client = inkBot(intents=intents)

with Path("info.json").open() as f:
    json = load(f)
token = json["token"]
client.run(token)
