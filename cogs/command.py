from discord.ext import commands
from core.classes import Cog_Extension


class Commands(Cog_Extension):

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot in ready")

    @commands.command()
    async def hello(self, ctx):
        """say hello"""
        await ctx.send(f"!Hi <@{ctx.author.id}>")

    @commands.command()
    async def say(self, ctx, *text):
        """get gpu temperature"""
        await ctx.send(" ".join(text))


async def setup(bot):
    await bot.add_cog(Commands(bot))
