import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')

    if message.content.startswith(".help"):
        e = discord.Embed(title='Help Message!')
        await message.channe.send("- Help sends this message", embed=e)
client.run('NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.LOwGMDOlV4ugDqRpoV75I6wpDcA')

# NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.MQ_fgVbcKW_-Tl0Td0rf9Gz5V_Q