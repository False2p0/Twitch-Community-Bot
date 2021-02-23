import discord
from discord.ext import commands
import asyncio

import datetime
import time
import os

from test import version
from test import dev_id

defualt_color = 0xfcfcfc

class info(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('Info is ready')
        print("---")

    @commands.command(aliases=["serverinfo"])
    async def serverstats(self, ctx):
        embed = discord.Embed(
            title=f"\n", color=0x8c45f7, timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.add_field(name="ID", value=f"{ctx.guild.id}")
        embed.add_field(name="Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Region", value=f"{ctx.guild.region}")
        embed.add_field(name="Member Count", value=f"{ctx.guild.member_count}")
        embed.add_field(name="Created at", value=f"{ctx.guild.created_at}")
        embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)


    @commands.command(aliases=["Botinfo"])
    async def botstats(self, ctx):
        embed = discord.Embed(title="\n",color=0x8c45f7, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.add_field(name="Bot version", value=version, inline=False)
        embed.add_field(name="Bot Name", value=self.client.user.name, inline=False)
        embed.add_field(name="Bot Nickname", value=self.client.user.display_name, inline=False)
        embed.add_field(name="Bot Avatar", value=F"[Avatar]({self.client.user.avatar_url})", inline=False)
        embed.add_field(name="Dev", value=f"<@{dev_id}>", inline=False)
        embed.add_field(name="Bot Discriminator", value=self.client.user.discriminator, inline=False)
        embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(info(client))