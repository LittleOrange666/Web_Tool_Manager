import json

from discord.ext import commands, tasks
from core.classes import Cog_Extension
from tools.publish import ToolManager

with open("tools.json") as f:
    tools = json.load(f)
managers = {k: ToolManager(k,**v) for k, v in tools.items()}


class Tools(Cog_Extension):
    @commands.command()
    async def stat(self, ctx):
        """get tools status"""
        print("getting tools status")
        l = ["id\tstat\turl\tshorturl"]
        for k, v in managers.items():
            print("get tools status for " + k)
            l.append(f'{k}\t{"Running" if v.isrunning() else "Stopped"}\t{v.geturl()}\t{v.getshorturl()}')
        print(l)
        print("complete getting tools status")
        await ctx.send("\n".join(l))

    @commands.command()
    async def start(self, ctx, id: str):
        """start tool"""
        if id not in managers:
            await ctx.send(f"unknown tool id {id!r}")
        else:
            obj = managers[id]
            if obj.isrunning():
                await ctx.send(f"tool id {id!r} already started")
            else:
                obj.start()
                await ctx.send(f"starting tool id {id!r}")
                obj.publisher.wait_completed()
                # obj.wait_completed()
                await ctx.send(f'URL: {obj.geturl()}\nShortURL: {obj.getshorturl()}')

    @commands.command()
    async def stop(self, ctx, id: str):
        """stop tool"""
        if id not in managers:
            await ctx.send(f"unknown tool id {id!r}")
        else:
            obj = managers[id]
            if not obj.isrunning():
                await ctx.send(f"tool id {id!r} already stopped")
            else:
                obj.stop()
                await ctx.send(f"stopping tool id {id!r}")

    @commands.command()
    async def restart(self, ctx, id: str):
        """restart tool"""
        if id not in managers:
            await ctx.send(f"unknown tool id {id!r}")
        else:
            obj = managers[id]
            if not obj.isrunning():
                await ctx.send(f"tool id {id!r} already stopped")
            else:
                obj.restart()
                obj.publisher.wait_completed()
                await ctx.send(f"restarted tool id {id!r}")

    @tasks.loop(seconds=1)
    async def checking(self):
        for k, v in managers.items():
            if v.running and v.shorturl is None:
                print("detected " + k)
                if v.getshorturl() is not None:
                    print(f"tool {k!r} started, shorturl: {v.shorturl}")
                    await self.bot.get_channel(688019708808658957).send(f"tool {k!r} started, shorturl: {v.shorturl}")
            l = []
            for k, v in managers.items():
                l.append(f'{k}\t{"Running" if v.isrunning() else "Stopped"}\t{v.geturl()}\t{v.getshorturl()}')
            print(l)

    @checking.before_loop
    async def before(self):
        await self.bot.wait_until_ready()
        print("Finished waiting")


async def setup(bot):
    await bot.add_cog(Tools(bot))
