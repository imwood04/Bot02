import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run('NjY0MDM3NDYxMjE4ODIwMTA2.XhRPEw.MQ_fgVbcKW_-Tl0Td0rf9Gz5V_Q')