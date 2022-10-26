import discord
from discord import app_commands
from discord.ext import commands

from pathlib import Path
from json import load

import random
import typing

with Path("utils/var_storage.json").open() as f:
    vars_json = load(f)
pickup_lines = vars_json["pickup_list"]
eightball_replies = vars_json["eightball_list"]


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def funcommands_ready(self) -> None:
        """Sign to show that the cog has loaded successfully"""
        print(f"{__class__.__name__} ready")

    @app_commands.command(name="say", description="Make the bot say something in a particular channel (channel "
                                                  "defaults to the current channel)")
    async def say(self,
                  interaction: discord.Interaction,
                  message: str,
                  channel: typing.Optional[discord.TextChannel] = None):
        """Make the bot send a particular message in a specified channel

        Parameters
        ----------

        interaction: `discord.Interaction`
            The interaction that's calling the command
        message: `str`
            The message for the bot to send
        channel: `discord.TextChannel`
            The channel to send the message in
            (Defaults to the channel that the interaction was called in)"""
        if channel is None:
            await interaction.response.send_message(message)
        else:
            if channel.permissions_for(interaction.user).send_messages:
                await channel.send(message)
                await interaction.response.send_message(f'Message has been sent in {channel.mention}', delete_after=5)
            else:
                await interaction.response.send_message(
                    f'Don\'t try making me say stuff in channels where you don\'t have perms '
                    f'<:lolnub:842673428695744522>')


# setup for the cog
async def setup(bot):
    await bot.add_cog(FunCommands(bot))
