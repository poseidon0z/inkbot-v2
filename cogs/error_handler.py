import traceback
import sys
from discord.ext import commands
import discord.ext.commands.errors as er


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # I don't have shit for partial emoji conversion faliure cause idfk what that is
    @commands.Cog.listener('on_command_error')
    async def global_error_handler(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = er.CommandNotFound
        missing_params = (er.MissingRequiredArgument, er.MissingRequiredAttachment)
        not_found = (er.MessageNotFound, er.MemberNotFound, er.GuildNotFound, er.UserNotFound,
                     er.ChannelNotFound, er.RoleNotFound, er.EmojiNotFound, er.GuildStickerNotFound,
                     er.ScheduledEventNotFound, er.ThreadNotFound)
        user_missing_perms = (er.MissingRole, er.MissingPermissions, er.MissingAnyRole)
        bot_missing_perms = (er.BotMissingPermissions, er.BotMissingRole, er.BotMissingAnyRole)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, missing_params):
            await ctx.reply(f"`{error.param}` is a required param that you failed to specify.")

        elif isinstance(error, er.TooManyArguments):
            await ctx.reply("Too many arguments given!")

        elif isinstance(error, not_found):
            await ctx.reply(f"{error.argument} not found...")

        elif isinstance(error, er.ChannelNotReadable):
            await ctx.reply(f"Sorry, I can't do this since I can't read messages in {error.argument}.")

        elif isinstance(error, er.BadColourArgument):
            await ctx.reply(f"{error.argument} is not a valid color.")

        elif isinstance(error, er.BadInviteArgument):
            await ctx.reply(f"The invite {error.argument} is invalid or expired.")

        elif isinstance(error, er.BadBoolArgument):
            await ctx.reply(f"Couldn't parse {error.argument} as a valid bool")

        elif isinstance(error, er.RangeError):
            await ctx.reply(f"{error.value} is out of range... please provide a value between {error.minimum} "
                            f"and {error.maximum}.")

        elif isinstance(error, user_missing_perms):
            await ctx.reply(f"You don't have permission to run this command.")

        elif isinstance(error, bot_missing_perms):
            await ctx.reply(f"I am not allowed to run this command (check if I lack permissions or roles to run this "
                            f"command)")

        elif isinstance(error, er.CheckFaliure):
            pass

        elif isinstance(error, er.DisabledCommand):
            await ctx.reply(f"This command is disabled.")

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


# set up the cog
async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
