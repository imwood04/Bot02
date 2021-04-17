import json

import discord
import random
from discord.ext import commands


async def get_bank_data():
    with open("mainBank.json", "r") as f:
        users = json.load(f)
    return users


async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        print(f'{user.id} Has been added to the Bank!')
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0
    with open('mainBank.json', 'w') as f:
        json.dump(users, f)
    return True


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def work(self, ctx):
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        wallet_amt = users[str(user.id)]['wallet']
        new_wall_amt = wallet_amt + random.randint(250, 9000)
        if str(user.id) in users:
            users[str(user.id)]['wallet'] = new_wall_amt
            await ctx.send(f'**You Worked a Successful Shift! Your new Balance is {new_wall_amt}!**')
        else:
            return False
        with open('mainBank.json', 'w') as f:
            json.dump(users, f)
        return True

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        wallet_amt = users[str(user.id)]['wallet']
        bank_amt = users[str(user.id)]['bank']

        em = discord.Embed(title=f"{ctx.author.name}'s balance!", color=discord.Color.blue())
        em.add_field(name="Wallet", value=wallet_amt)
        em.add_field(name="Bank", value=bank_amt)
        em.set_footer(text="Bot made by: ZeroTwo#8676")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Economy(bot))
