import discord
import random
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
# Prefix for commands!
client = commands.Bot(command_prefix=".", intents=intents)


# Lets you know if bot is Running!
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Watching Anime!'))
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    print(f'{member} Has joined the Server!')


@client.event
async def on_member_remove(member):
    print(f'{member} Has left the Server!')


@client.command()
async def hello(ctx):
    await ctx.send('Hello!')


# Ping Command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# 8ball Command
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        'Yes', 'No', "Definitely", "Probably Not", "Possibly", "Don't Count on it"
    ]
    await ctx.send(f'Question: {question}\n\nAnswer: {random.choice(responses)}')


# Purge Command
@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@purge.error
async def purgeError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify an Amount!')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Missing Permissions!')


# roll Command
@client.command()
async def roll(ctx, *, choice: int):
    responses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    if choice >= 11:
        await ctx.send('Pick between 1-10')
    else:
        await ctx.send(f'You Choose: {choice}\nRolled: {random.choice(responses)}')


@roll.error
async def rollError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Pick a number between 1-10')
client.run('NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.LOwGMDOlV4ugDqRpoV75I6wpDcA')

# NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.MQ_fgVbcKW_-Tl0Td0rf9Gz5V_Q
