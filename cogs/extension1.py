import discord
from discord.ext import commands

class example(commands.Cog):
    def __int__(self, client):
        self.client = client
def setup(client):
    client.add_cog(example(client))