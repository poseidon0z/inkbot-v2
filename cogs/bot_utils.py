import time
import typing
from json import load
from pathlib import Path

import discord
import pymongo
from discord.ext import commands

from utils.checks import not_banned_cmd

with Path("info.json").open() as f:
    info = load(f)
client_code = info['mongo_client']
mongo_client = pymongo.MongoClient(client_code)
ban_location = mongo_client['bot_data']['banned_users']


class BotUtil(commands.Cog):
    """This cog consists of util commands for ink

    Commands
    --------

    sync
        Sync all slash commands globally

    alive
        Check if the bot is alive

    ban
        Ban users from the bot

    unban
        Unban users from the bot

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def botutil_ready(self) -> None:
        """Sign to show that the cog has loaded successfully"""
        print(f"{__class__.__name__} ready")

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        """Globally syncs all slash commands

        Parameters
        -------

        ctx: `commands.Context`
            Context in which command was called"""
        print("Commands syncing")

        try:
            synced = await self.bot.tree.sync()
        except Exception as e:
            print(e)

        channel = self.bot.get_channel(838425596421079060)
        await ctx.send(f"{self.bot.user} ({self.bot.user.id}) has synced {len(synced)} commands successfully!")
        await channel.send(f"{self.bot.user} ({self.bot.user.id}) has synced {len(synced)} commands successfully!")
        print("Commands synced successfully")

    @commands.command(name="alive")
    @not_banned_cmd()
    async def alive(self, ctx) -> None:
        """Say "I'm alive" in response to message sent
        Used to check if bot is alive

        Parameters
        -------

        ctx: `commands.Context`
            Context in which command was called"""
        await ctx.send("I'm alive")

    @commands.command(name="ban")
    @commands.is_owner()
    async def ban(self, ctx, target: discord.User, *, reason: typing.Optional[str] = None) -> None:
        """Ban members
        Banned members are blocked from using all bot commands

        Parameters
        -------

        ctx: `commands.Context`
            Context in which command was called
        target: `discord.User`
            The user to be banned
        reason: `str`
            Reason for the ban (noted in logs)"""

        if reason is None:
            reason = "No reason provided"

        result = ban_location.find_one({"user_id": target.id})
        if result is not None:
            banned_by = result["banned_by"]
            time_banned = int(result["time"])
            reason = result["reason"]
            await ctx.send(
                f"The user has already been banned by <@{banned_by}> at <t:{time_banned}:F> with reason: `{reason}`")
            return

        post = {"user_id": target.id,
                "reason": reason,
                "time": time.time(),
                "banned_by": ctx.author.id}
        ban_location.insert_one(post)

        await ctx.send(f"Banned {target} ({target.id}) with the reason: `{reason}`")

    @commands.command(name="unban")
    @commands.is_owner()
    async def unban(self, ctx, target: discord.User, reason: typing.Optional[str] = None) -> None:
        """Unban a previously banned user

        Parameters
        -------

        ctx: `commands.Context`
            Context in which command was called
        target: `discord.User`
            The user to be unbanned
        reason: `str`
            Reason for the unban (noted in logs)"""
        if reason is None:
            reason = "No reason provided"

        result = ban_location.find_one({"user_id": target.id})
        if result is not None:
            ban_location.delete_one(result)
            await ctx.send(f"Unbanned <@{target.id}>")
        else:
            await ctx.send("This user is not banned....")


# set up the cog
async def setup(bot):
    await bot.add_cog(BotUtil(bot))
