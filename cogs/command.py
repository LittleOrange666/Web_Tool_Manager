from discord.ext import commands
from core.classes import Cog_Extension
import pynvml

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)


class Commands(Cog_Extension):

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot in ready")

    @commands.command()
    async def hello(self, ctx):
        """say hello"""
        await ctx.send(f"!Hi <@{ctx.author.id}>")

    @commands.command()
    async def temp(self, ctx):
        """get gpu temperature"""
        await ctx.send(f"{pynvml.nvmlDeviceGetTemperature(handle, 0)}°C")

    @commands.command()
    async def say(self, ctx, *text):
        """get gpu temperature"""
        await ctx.send(" ".join(text))


async def setup(bot):
    await bot.add_cog(Commands(bot))
