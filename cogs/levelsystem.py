import discord
from discord.ext import commands
from pymongo import MongoClient

bot_channel = 882420889675771914
talk_channel = [882407949669122110, 882408002118885437, 889264568415703050, 883923791720349717, 884963283407355985, 882408243236839485, 882421939250032723, 890028918747328532, 902785816839983187, 882408025485365248]

level_roles = ['Member Lvl 5']
level_num = [5]

cluster = MongoClient(
    "mongodb+srv://imwood04:CmjnxSxGO6nsl0JW@02.kbi7i.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

leveling = cluster["menudocs"]["leveling"]


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channel:
            stats = leveling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "xp": 100}
                    leveling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    leveling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50 * (lvl ** 2)) + (50 * (lvl))):
                            break
                        lvl += 1
                    xp -= ((50 * (lvl - 1)) + (50 * (lvl - 1)))

                    if xp == 0:
                        await message.channel.send(
                            f'Congrats {message.author.mention}! YOu Leveled up to **level {lvl}**')
                        for i in range(len(level_roles)):
                            if lvl == level_num[i]:
                                await message.author.add_roles(
                                    discord.utils.get(message.author.guild.roles, name=level_roles[i]))
                                embed = discord.Embed(
                                    description=f'{message.author.mention} you have earned **{level_roles[i]}**!!')
                                embed.set_thumbnail(url=message.author.avatar.url)
                                await message.channel.send(embed=embed)

    @commands.command(description="Only works in my discord Rn!")
    async def rank(self, ctx):
        if ctx.channel.id == bot_channel:
            stats = leveling.find_one({"id": ctx.author.id})
            if stats is None:
                embed = discord.Embed(description="You Haven't done anything for a Rank!")
                await ctx.channel.send(embed=embed)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                        break
                    lvl += 1
                xp -= ((50 * (lvl - 1)) + (50 * (lvl - 1)))
                boxes = int((xp / (200 * ((1 / 2) * lvl))) * 20)
                rankings = leveling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats['id'] == x['id']:
                        break
                embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
                embed.add_field(name='Name', value=ctx.author.mention, inline=True)
                embed.add_field(name='XP', value=f'{xp}/{int(200 * ((1 / 2) * lvl))}', inline=True)
                embed.add_field(name='Level', value=f'{lvl}', inline=True)
                embed.add_field(name='Rank', value=f'{rank}/{ctx.guild.member_count}', inline=True)
                embed.add_field(name='Progress Bar [lvl]', value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)

    @commands.command(description="Only works in my discord Rn!")
    async def leaderboard(self, ctx):
        if (ctx.channel.id == bot_channel):
            rankings = leveling.find().sort("xp", -1)
            i = 1
            embed = discord.Embed(title="Rankings!")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f'{i}: {temp.name}', value=f'Total XP: {tempxp}', inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(LevelSystem(bot))
