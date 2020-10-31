import discord
import random
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
# Prefix for commands!
client = commands.Bot(command_prefix=".", intents=intents)


# Lets you know if bot is Running!
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

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
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

client.run('NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.LOwGMDOlV4ugDqRpoV75I6wpDcA')

# NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.MQ_fgVbcKW_-Tl0Td0rf9Gz5V_Q
