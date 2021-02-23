import discord
from discord.ext import commands
import asyncio
import datetime
import time
import os
import json

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from pprint import pprint


twitch = Twitch('') # Twitch Api Token


class twitchtest(commands.Cog):

    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_ready(self):
        print('twitch is ready')
        print("---")

    @commands.command()
    async def twitchinfo(self, ctx):
        embed = discord.Embed(title="send your Twitch name")
        sent = await ctx.send(embed=embed)
        try:
            msg = await self.client.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel)
            if msg:
                name = msg.content
                await sent.delete()
                await msg.delete()
                twitch.authenticate_app([])
                print(name.lower())
                data = (twitch.get_users(logins=[f'{name.lower()}']))
                pprint(data)
                embed = discord.Embed(title=f"Infos about {name} ", description=data['data'][0]['description'],color=0x8c45f7, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="Name:", value=f"{data['data'][0]['display_name']}", inline=False)
                embed.add_field(name="Views:", value=data['data'][0]['view_count'], inline=False)
                embed.add_field(name="Created at:", value=data['data'][0]['created_at'], inline=False)
                embed.set_image(url=data['data'][0]['offline_image_url'])
                embed.set_thumbnail(url=data['data'][0]['profile_image_url'])
                embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
                await ctx.send(embed=embed)


        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Chancelling due to timeout.", delete_after=10)
        
        

    @commands.command()
    async def topgame(self, ctx):
        twitch.authenticate_app([])
        x = twitch.get_top_games()
        pprint(x)
        embed = discord.Embed(title="Top Games on Twitch",color=0x8c45f7, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="1", value=x['data'][0]['name'], inline=False)
        embed.add_field(name="2", value=x['data'][1]['name'], inline=False)
        embed.add_field(name="3", value=x['data'][2]['name'], inline=False)
        embed.add_field(name="4", value=x['data'][3]['name'], inline=False)
        embed.add_field(name="5", value=x['data'][4]['name'], inline=False)
        embed.add_field(name="6", value=x['data'][5]['name'], inline=False)
        embed.add_field(name="7", value=x['data'][6]['name'], inline=False)
        embed.add_field(name="8", value=x['data'][7]['name'], inline=False)
        embed.add_field(name="9", value=x['data'][8]['name'], inline=False)
        embed.add_field(name="10", value=x['data'][9]['name'], inline=False)
        y = x['data'][0]['box_art_url']
        url_pictur1 = str(y).replace('{width}', '500')
        url_pictur2 = str(url_pictur1).replace('{height}', '600')
        embed.set_thumbnail(url=url_pictur2)
        embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def Game(self, ctx):
        embed = discord.Embed(title="send your Twitch name")
        sent = await ctx.send(embed=embed)
        try:
            msg = await self.client.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel)
            if msg:
                name = msg.content
                await sent.delete()
                await msg.delete()
                twitch.authenticate_app([])
                print(name.lower())
                x = twitch.get_games(names=f'{name}')
                embed = discord.Embed(title=f" {name} ",color=0x8c45f7, timestamp=datetime.datetime.utcnow())
                y = x['data'][0]['box_art_url']
                url_pictur1 = str(y).replace('{width}', '500')
                url_pictur2 = str(url_pictur1).replace('{height}', '600')
                embed.set_image(url=url_pictur2)
                embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
                await ctx.send(embed=embed)


        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Chancelling due to timeout.", delete_after=10)


def setup(client):
    client.add_cog(twitchtest(client))