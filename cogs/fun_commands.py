import discord
from discord import app_commands
from discord.ext import commands

from pathlib import Path
from json import load

import random
import typing

from utils.checks import not_banned_slash

with Path("utils/var_storage.json").open(encoding="utf8") as f:
    vars_json = load(f)
pickup_lines = vars_json["pickup_list"]
eightball_replies = vars_json["eightball_list"]
descriptions = vars_json["description_list"]

with Path("utils/design.json").open() as f:
    design = load(f)
base_color = int(design["embed"]["base_color"], base=16)


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def funcommands_ready(self) -> None:
        """Sign to show that the cog has loaded successfully"""
        print(f"{__class__.__name__} ready")

    @app_commands.command(name="say")
    @not_banned_slash()
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
            return

        if not channel.permissions_for(interaction.user).send_messages:
            await interaction.response.send_message("Don't try making me say stuff in channels where you don't have "
                                                    "perms <:lolnub:842673428695744522>")
            return
        await interaction.response.send_message(f"Sending the message in {channel.mention}")
        await channel.send(message)

    @app_commands.command(name="iq")
    @not_banned_slash()
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

        iq = random.randint(a=40, b=160)

        if target.id == 652756616185380894:  # rigging it for myself
            iq = 160

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

    @app_commands.command(name="describe")
    @not_banned_slash()
    async def describe(self, interaction: discord.Interaction, target: typing.Optional[discord.User] = None) -> None:
        """Describe a user (describe user calling the command if no one specified)

        Parameters
        ---------

        interaction: `discord.Interaction`
            The interaction that's calling the command
        target: `discord.User`
            The user to describe
            (Defaults to command invoker)"""
        if target is None:
            target = interaction.user

        description = random.choice(descriptions)

        if target.id == 652756616185380894:
            description = "amazing"

        await interaction.response.send_message(f"{target.mention} is {description}!",
                                                allowed_mentions=discord.AllowedMentions.none())

    @app_commands.command(name="besmooth")
    @not_banned_slash()
    async def be_smooth(self, interaction: discord.Interaction):
        """Use a random pickup line

        Parameters
        ----------

        interaction: `discord.Interaction`
            The interaction that's calling the command
        """
        message = random.choice(pickup_lines)
        await interaction.response.send_message(message)

    @app_commands.command(name="8ball")
    @not_banned_slash()
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        """Ask any question to the magic 8 ball

        Parameters
        ---------

        interaction: `discord.Interaction`
            The interaction that's calling the command
        question: `str`
            What to ask the magic 8-ball
        """
        ball_response = random.choice(eightball_replies)
        await interaction.response.send_message(f":crystal_ball:{ball_response}, {interaction.user.mention}")

    @app_commands.command(name="choose")
    @not_banned_slash()
    async def choose(self, interaction: discord.Interaction, choices: str):
        """Ask any question to the magic 8 ball

        Parameters
        ---------

        interaction: `discord.Interaction`
            The interaction that's calling the command
        choices: `str`
            Choices among which to choose one, separated bt commas
        """
        choices_list = choices.split(",")
        choice = random.choice(choices_list)
        await interaction.response.send_message(f"Out of {choices}, \nI choose {choice}")


# set up the cog
async def setup(bot):
    await bot.add_cog(FunCommands(bot))
