import json

from discord.ext import commands, tasks
from core.classes import Cog_Extension
from tools.publish import ToolManager

with open("tools.json") as f:
    tools = json.load(f)
managers = {k: ToolManager(k, **v) for k, v in tools.items()}


class Tools(Cog_Extension):
    @commands.command()
    async def stat(self, ctx):
        """get tools status"""
        print("getting tools status")
        out_lines = ["id\tstat\turl\tshorturl"]
        for k, v in managers.items():
            print("get tools status for " + k)
            out_lines.append(f'{k}\t{"Running" if v.isrunning() else "Stopped"}\t{v.geturl()}\t{v.getshorturl()}')
        print(out_lines)
        print("complete getting tools status")
        await ctx.send("\n".join(out_lines))

    @commands.command()
    async def start(self, ctx, tid: str):
        """start tool"""
        if tid not in managers:
            await ctx.send(f"unknown tool id {tid!r}")
        else:
            obj = managers[tid]
            if obj.isrunning():
                await ctx.send(f"tool id {tid!r} already started")
            else:
                obj.start()
                await ctx.send(f"starting tool id {tid!r}")
                obj.publisher.wait_completed()
                # obj.wait_completed()
                await ctx.send(f'URL: {obj.geturl()}\nShortURL: {obj.getshorturl()}')

    @commands.command()
    async def stop(self, ctx, tid: str):
        """stop tool"""
        if tid not in managers:
            await ctx.send(f"unknown tool id {tid!r}")
        else:
            obj = managers[tid]
            if not obj.isrunning():
                await ctx.send(f"tool id {tid!r} already stopped")
            else:
                obj.stop()
                await ctx.send(f"stopping tool id {tid!r}")

    @commands.command()
    async def restart(self, ctx, tid: str):
        """restart tool"""
        if tid not in managers:
            await ctx.send(f"unknown tool id {tid!r}")
        else:
            obj = managers[tid]
            if not obj.isrunning():
                await ctx.send(f"tool id {tid!r} already stopped")
            else:
                obj.restart()
                await ctx.send(f"restarted tool id {tid!r}")

    @commands.command()
    async def relink(self, ctx, tid: str):
        """restart tool"""
        if tid not in managers:
            await ctx.send(f"unknown tool id {tid!r}")
        else:
            obj = managers[tid]
            if not obj.isrunning():
                await ctx.send(f"tool id {tid!r} already stopped")
            else:
                obj.publisher.restart()
                await ctx.send(f"relinked tool id {tid!r}")

    @tasks.loop(seconds=1)
    async def checking(self):
        for k, v in managers.items():
            if v.running and v.shorturl is None:
                print("detected " + k)
                if v.getshorturl() is not None:
                    print(f"tool {k!r} started, shorturl: {v.shorturl}")
                    await self.bot.get_channel(688019708808658957).send(f"tool {k!r} started, shorturl: {v.shorturl}")
            l = []
            for k0, v0 in managers.items():
                l.append(f'{k0}\t{"Running" if v0.isrunning() else "Stopped"}\t{v0.geturl()}\t{v0.getshorturl()}')
            print(l)

    @checking.before_loop
    async def before(self):
        await self.bot.wait_until_ready()
        print("Finished waiting")


async def setup(bot):
    await bot.add_cog(Tools(bot))
