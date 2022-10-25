import discord
from discord.ext import commands


class botUtil(commands.Cog):
    """This cog consists of util commands for ink

    Commands
    --------

    Sync 
        Sync all slash commands globally
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
        """Globally syncs all slash commands"""
        print("Commands syncing")

        try:
            synced = await self.bot.tree.sync()
        except Exception as e:
            print(e)

        channel = self.bot.get_channel(838425596421079060)
        await channel.send(f"{self.bot.user} ({self.bot.user.id}) has synced {len(synced)} commands successfully!")
        print("Commands synced successfully")


# running the setup for the cog
async def setup(bot):
    await bot.add_cog(botUtil(bot))
