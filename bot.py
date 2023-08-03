import asyncio
import os

from discord.ext import commands
import discord
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

with open('token.json', "r", encoding="utf8") as file:
    data = json.load(file)


@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")


# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    """load extension"""
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    """unload extension"""
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")


# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    """reload extension"""
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")


# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(data['token'])

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())
