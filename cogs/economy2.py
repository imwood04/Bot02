import random

import discord
from discord.ext import commands
from pymongo import MongoClient

import bot

cluster = MongoClient(
    "mongodb+srv://imwood04:CmjnxSxGO6nsl0JW@02.kbi7i.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

leveling = cluster["menudocs"]["eco"]
prefix = cluster["menudocs"]["config"]


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

    @commands.command(name='Work', description='Make your Earnings')
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def work(self, ctx):
        user = ctx.author

        check = leveling.find_one({"id": user.id})
        if check is None:

            await ctx.message.reply(
                "You don't have a profile!\nPlease execute the `!create` command to create a profile!")
            return

        else:

            job_names = ["Cashier", "McDonald's Worker", "Criminal", "Retail Worker", "Mechanic"]
            job = random.choice(job_names)

            amount = random.randint(100, 1000)
            new_bal = check['money'] + amount

            leveling.update_one({"id": user.id}, {"$set": {"money": new_bal}})

            em = discord.Embed(
                title="You have finished working!",
                description=f"You have worked as a **{job}** and earned **${amount}**!",
                color=discord.Colour.random()
            )

            await ctx.message.reply(embed=em)
            return

    # noinspection PyBroadException
    @commands.command(name='Baltop', description='Shows the Balance Leaderboard!', aliases=["bt"])
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def baltop(self, ctx):
        user = ctx.author
        channel = ctx.channel.id
        if ctx.channel.id == channel:
            check = leveling.find_one({"id": user.id})
            create = ''
            if check is None:
                await ctx.message.reply(
                    "You don't have a profile!\nPlease execute the `!create` command to create a profile!")
                return
            rankings = leveling.find().sort("money", -1)
            i = 1
            embed = discord.Embed(title="Top 10 Balances!")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["money"]
                    embed.add_field(name=f'{i}: {temp.name}', value=f'Total Money: {tempxp}', inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy2(bot))
