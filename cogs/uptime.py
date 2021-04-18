import discord, datetime, time

from discord.ext import commands

# get the bots time when it starts
start_time = time.time()


class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='uptime', description='Want Uptime use the Command', pass_context=True)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=ctx.message.author.top_role.colour)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="Bot made by: ZeroTwo#8676")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)


def setup(bot):
    bot.add_cog(Uptime(bot))
