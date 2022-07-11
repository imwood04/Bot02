import json
import random

from pymongo import MongoClient
import discord
from discord.ext import commands

cluster = MongoClient(
    "mongodb+srv://imwood04:CmjnxSxGO6nsl0JW@02.kbi7i.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

leveling = cluster["menudocs"]["eco"]


class Economy2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='create', description='Create a bank Account!', aliases=['ct'])
    async def create(self, ctx):
        user = ctx.author

        check = leveling.find_one({"id": user.id})

        if check is None:
            insert = {
                "id": user.id, "name": user.name, "tags": user.discriminator, "money": 100
            }

            leveling.insert_one(insert)

            await ctx.message.reply(f"Profile Successfully Created for {user.name}")
            return

        else:
            await ctx.message.reply("You Only Needed to do this Once")
            return

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, user: discord.Member = None):
        author = ctx.author

        if user is None:
            check = leveling.find_one({"id": author.id})

            if check is None:
                await ctx.message.reply(
                    "You don't have a profile!\nPlease execute the `?create` command to create a profile!")
                return

            else:
                balance = check['money']

                em = discord.Embed(
                    title="Your balance!",
                    description=f"**Balance:** ${balance}",
                    color=discord.Colour.random()
                )

                await ctx.message.reply(embed=em)
                return

        else:
            check = leveling.find_one({"id": user.id})

            if check is None:
                await ctx.message.reply("The user you have mentioned does not have a profile!")
                return

            else:
                balance = check['money']

                em = discord.Embed(
                    title=f"{user.name}'s Balance!",
                    description=f"**Balance:** ${balance}",
                    color=discord.Colour.random()
                )

                await ctx.message.reply(embed=em)
                return


def setup(bot):
    bot.add_cog(Economy2(bot))
