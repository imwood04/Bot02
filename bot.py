import os
import random
import rule34
import json
import discord
from discord.ext import commands
from discord import File

rule34 = rule34.Sync()
rule34.getImages("SearchQuery")
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)

client = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True)
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


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Please Type a Valid Command!')


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def hello(ctx):
    await ctx.send('Hello!')


# Ping Command
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# 8ball Command
@client.command(aliases=['8ball'])
@commands.cooldown(1, 5, commands.BucketType.user)
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
@commands.cooldown(1, 5, commands.BucketType.user)
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
@commands.cooldown(1, 5, commands.BucketType.user)
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
@commands.guild_only()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def kick(ctx, *, reason=None):
    member = ctx.message.author
    await member.kick(reason=reason)


@client.command()
@commands.guild_only()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@client.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def unban(self, ctx, userId):
    user = discord.Object(id=userId)
    await ctx.guild.unban(user)
    await ctx.send(f"Unbanned {user}")


# Help Message
@client.command()
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):
    embed = discord.Embed(title="General Commands",
                          description="- Help >> Sends This Message!\n"
                                      "- 8ball >> Ask it anything!\n"
                                      "- Roll >> Choose a Number 1-10 and Roll\n"
                                      "- Ping >> Tells you the Bots Ping\n"
                                      "- avatar >> Steals pinged users avatar\n"
                                      "- spank >> ping someone to spank them!\n"
                                      "- hug >> ping someone to hug them!\n"
                                      "- serverinfo >> gives basic server info!\n"
                                      "- invite >> sends bots invite link\n"
                                      "- balance >> Tells You Your Balance!",
                          color=discord.colour.Colour.dark_blue())
    embed.add_field(name="Admin Commands", value="- Purge \n - Kick \n - Ban", inline=False)
    embed.add_field(name="Gambling Commands",
                    value="- coinflip >> Flips a Coin\n - roulette >> 1/6 Chance of being shot DEAD!\n")
    embed.set_footer(text="Bot made by: ZeroTwo#8676 ")
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
                                       "- coinflip >> Flips a Coin\n"
                                       "- roulette >> 1/6 Chance of being shot DEAD!\n"
                                       "- spank >> ping someone to spank them!\n"
                                       "- hug >> ping someone to give them a hug1\n"
                                       "- serverinfo >> gives basic server info!\n"
                                       "- invite >> sends bots invite link!\n"
                                       "- balance >> Tells You Your Balance!",
                           color=discord.colour.Colour.dark_blue())
    embed1.set_footer(text="Bot made by: ZeroTwo#8676 ")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=embed1)


@client.command(aliases=['av'])
@commands.cooldown(1, 5, commands.BucketType.user)
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
# @commands.cooldown(1, 5, commands.BucketType.user)
async def coinflip(ctx, *, choice):
    HorT = ['Heads', 'Tails']
    random_response = random.choice(HorT)
    if random_response == choice:
        await ctx.send(f'You Won! it was {random_response}')
    else:
        await ctx.send(f'You Lost! it was {random_response}')


@client.command()
@commands.has_permissions(manage_roles=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def addrole(ctx, role: discord.Role, user: discord.Member):
    await user.add_roles(role)


@addrole.error
async def addroleError(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do Not have Permission to use this Command!')


@client.command()
@commands.has_permissions(manage_roles=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def delrole(ctx, role: discord.Role, user: discord.Member):
    await user.remove_roles(role)


@delrole.error
async def avatarError(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do Not have Permission to use this Command!')


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def aeveryone(ctx):
    member = ctx.message.author
    if ctx.author.id == 380153305394839554:
        await ctx.send(f'{member} said @everyone')


@kick.error
async def kickError(ctx, error):
    member = ctx.message.author
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{member} is Missing Perms!')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send('Bot is missing Perms!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing Arguments!')


@client.command(aliases=['rr'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def roulette(ctx):
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


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def spank(ctx, *, member: discord.Member):
    member1 = ctx.message.author
    diR = "gif/spank"
    gif = random.choice(os.listdir(diR))
    with open(f'{diR}\\{gif}', 'rb') as f:
        await ctx.send(f'{member1} has Spanked {member}')
        await ctx.send(file=File(f))


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def hug(ctx, *, member: discord.Member):
    member1 = ctx.message.author
    await ctx.send(f'{member1} has hugged {member}!')


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def invite(ctx):
    embed = discord.Embed(title="Click to invite!",
                          url="https://discord.com/api/oauth2/authorize?client_id=664037461218820106&permissions=8&scope=bot",
                          color=discord.colour.Colour.dark_red())
    embed.set_footer(text="Bot made by: ZeroTwo#8676")
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def serverinfo(ctx):
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
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=iD, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    await ctx.send(embed=embed)


##TODO Balance Command

@client.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    wallet_amt = users[str(user.id)]['wallet']
    if str(user.id) in users:
        users[str(user.id)]['wallet'] = wallet_amt + random.randint(250, 5000)
        await ctx.send('You Worked a Successful Shift!')
    else:
        return False
    with open('mainBank.json', 'w') as f:
        json.dump(users, f)
    return True


@work.error
async def workError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is not ready to use, try again in  %.2f seconds' % error.retry_after)
        return


@client.command(aliases=['bal'])
async def balance(ctx):
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


async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0
    with open('mainBank.json', 'w') as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("mainBank.json", "r") as f:
        users = json.load(f)
    return users


@client.command(aliases=["lb"])
async def leaderboard(ctx, x=1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f"Top 5 Richest People",
                       description="Top Richest Players in de Bot!",
                       color=discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        em.set_footer(text="Bot made by: ZeroTwo#8676")
        if index == x:
            index += 5
        else:
            index += 5

    await ctx.send(embed=em)


client.run('NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.LOwGMDOlV4ugDqRpoV75I6wpDcA')
# NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.MQ_fgVbcKW_-Tl0Td0rf9Gz5V_Q
