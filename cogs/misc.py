import asyncio
import platform
import random

import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name="stats", description="A useful command that displays bot statistics."
    )
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="\uFEFF",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Bot Version:", value=self.bot.version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        # noinspection PyTypeChecker
        embed.add_field(name="Total Guilds:", value=serverCount)
        # noinspection PyTypeChecker
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="<@380153305394839554>")

        embed.set_footer(text=f"Zero Two | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(
        name="echo",
        description="A simple command that repeats the users input back to them.",
    )
    async def echo(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title="Please tell me what you want me to repeat!",
            description="||This request will timeout after 1 minute.||",
        )
        sent = await ctx.send(embed=embed)

        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel,
            )
            if "@everyone" in msg.content:
                await ctx.send("Nice Try!")
                return
            elif msg:
                await sent.delete()
                await msg.delete()
                await ctx.send(msg.content)
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling", delete_after=10)

    @commands.command(
        name="toggle", description="Enable or disable a command!"
    )
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)

        if command is None:
            await ctx.send("I can't find a command with that name!")

        elif ctx.command == command:
            await ctx.send("You cannot disable this command.")

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"I have {ternary} {command.qualified_name} for you!")

    @commands.command(
        name='ping', description='Gets the bots Ping!'

    )
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command(name='avatar', description='Steals someones Avatar', aliases=['av'])
    async def avatar(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        userAvatar = member.avatar_url
        await ctx.send(userAvatar)

    @commands.command(name='serverinfo', description='Shows you the Serverinfo')
    async def serverinfo(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        owner = str(ctx.guild.owner)
        iD = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=random.choice(self.bot.color_list)
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=iD, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
