import discord
import random
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='8ball', description="Have o'l Great 8ball answer")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _8ball(self, ctx, *, question):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.", "You may rely on it.",
            "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
            "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."
        ]
        await ctx.send(f'Question: {question}\n\nAnswer: ||{random.choice(responses)}||')


    @commands.command(name='coinflip', description='', aliases=['cf'])
    async def coinflip(self, ctx, *, choice):
        HorT = ['Heads', 'Tails']
        random_response = random.choice(HorT)
        if random_response == choice:
            await ctx.send(f'You Won! it was {random_response}')
        else:
            await ctx.send(f'You Lost! it was {random_response}')


    @commands.command(name='roulette', description='Test Your Luck', aliases=['rr'])
    async def roulette(self, ctx):
        member = ctx.message.author
        responses = "click", "click", "click", "click", "click", "BANG"
        responses1 = "Ooooh so lucky!", "has survived for today!", "you got lucky!"
        responses2 = "Better luck next time", "dang that must suck...", "RIP", "..wont be at your funeral."
        random_response = random.choice(responses)
        embed1 = discord.Embed(title="Roulette",
                               description=f"{member} {random_response} {random.choice(responses2)}",
                               color=discord.colour.Colour.dark_red())
        embed1.set_footer(text="Bot made by: ZeroTwo#8676 ")
        embed2 = discord.Embed(title="Roulette",
                               description=f"{member} {random.choice(responses1)}",
                               color=discord.colour.Colour.dark_blue())
        embed2.set_footer(text="Bot made by: ZeroTwo#8676 ")
        if random_response == "BANG":
            await ctx.send(embed=embed1)
        else:
            await ctx.send(embed=embed2)


    @commands.command(name='roll', description='Pick a Number 1-10 and Roll')
    async def roll(self, ctx, *, choice: int):
        responses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if choice >= 11:
            await ctx.send('Pick between 1-10')
        else:
            await ctx.send(f'You Choose: {choice}\nRolled: {random.choice(responses)}')


def setup(bot):
    bot.add_cog(Fun(bot))
