import random
import rule34
import discord
from discord.ext import commands

rule34 = rule34.Sync()
rule34.getImages("SearchQuery")
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)

client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')


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
        "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.", "You may rely on it.",
        "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.",
        "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
        "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."
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


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(self, ctx, userId):
    user = discord.Object(id=userId)
    await ctx.guild.unban(user)
    await ctx.send(f"Unbanned {user}")


# Help Message
@client.command()
@commands.has_permissions(manage_messages=True)
async def help(ctx):
    embed = discord.Embed(title="Commands",
                          description="- Help >> Sends This Message!\n"
                                      "- 8ball >> Ask it anything!\n"
                                      "- Roll >> Choose a Number 1-10 and Roll\n"
                                      "- Ping >> Tells you the Bots Ping\n"
                                      "- Ban >> Bans People\n"
                                      "- Kick >> Kicks People!\n"
                                      "- Purge >> Purges Messages!"
                                      "- avatar >> Steals pinged users avatar\n"
                                      "- coinflip >> Flips a Coin",
                          color=discord.colour.Colour.dark_blue())
    embed.set_footer(text="Bot made by: Zero Two#8676 ")
    if True:
        await ctx.send(embed=embed)


@help.error
async def helpError(ctx, error):
    embed1 = discord.Embed(title="Commands",
                           description="- Help >> Sends This Message!\n"
                                       "- 8ball >> Ask it anything!\n"
                                       "- Roll >> Choose a Number 1-10 and Roll\n"
                                       "- Ping >> Tells you the Bots Ping\n"
                                       "- avatar >> Steals pinged users avatar\n"
                                       "- coinflip >> Flips a Coin",
                           color=discord.colour.Colour.dark_blue())
    embed1.set_footer(text="Bot made by: Zero Two#8676 ")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=embed1)


@client.command(aliases=['av'])
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)


@avatar.error
async def avatarError(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Please Ping Someone!')


@client.command(aliases=['cf'])
async def coinflip(ctx):
    HorT = ['Heads', 'Tails']
    await ctx.send(f'Coin Landed on {random.choice(HorT)}!')


@client.command()
async def addrole(ctx, role: discord.Role, user: discord.Member):
    await user.add_roles(role)


@client.command()
async def delrole(ctx, role: discord.Role, user: discord.Member):
    await user.remove_roles(role)
client.run('NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.LOwGMDOlV4ugDqRpoV75I6wpDcA')

# NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.MQ_fgVbcKW_-Tl0Td0rf9Gz5V_Q
