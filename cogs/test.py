import discord
from discord.ext import commands
import asyncio
import datetime
import time
import os

class test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('test is ready')
        print("---")

    # command
    @commands.command()
    async def Ping(self, ctx):
        await ctx.send(F"Pong! {round(self.client.latency * 1000)}ms")



def setup(client):
    client.add_cog(test(client))