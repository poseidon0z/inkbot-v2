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

with Path("utils/design.json").open() as f:
    design = load(f)
base_color = int(design["embed"]["base_color"],base=16)


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def funcommands_ready(self) -> None:
        """Sign to show that the cog has loaded successfully"""
        print(f"{__class__.__name__} ready")

    @app_commands.command(name="say")
    async def say(self,
                  interaction: discord.Interaction,
                  message: str,
                  channel: typing.Optional[discord.TextChannel] = None):
        """Send a particular message in a specified channel anonymously (sends in channel where command was invoked
        if no channel specified)

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

    @app_commands.command(name="iq")
    async def iq(self,
                 interaction: discord.Interaction,
                 target: typing.Optional[discord.User] = None):
        """Show iq of a user (Shows iq of person calling command if no target is specified)

        Parameters
        ---------

        interaction: `discord.Interaction`
            The interaction that's calling the command
        target: `discord.User`
            The target who's iq is to be found
            (Defaults to command invoker)"""

        # set target as the command invoker if no target is specified
        if target is None:
            target = interaction.user

        if target.id == 652756616185380894:  # rigging it for myself by making my iq always 160
            iq = 160
        else:  # the actual function
            iq = random.randint(a=40, b=160)

        # setting an emote to be displayed in embed according to iq
        if iq >= 116:
            emote = '<:bigbrain:838472543705759824>'
        elif iq >= 84:
            emote = ':brain:'
        elif iq >= 40:
            emote = '<:dumbfuck:838730636175998976>'

        iq_embed = discord.Embed(title=f'{target.name}\'s iq:',
                                 description=f'{target.mention} has an iq of {iq} {emote}',
                                 color=base_color)
        await interaction.response.send_message(embed=iq_embed)


# setup for the cog
async def setup(bot):
    await bot.add_cog(FunCommands(bot))
