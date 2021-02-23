import discord
from discord.ext import commands
import asyncio
import wikipedia

import random

import aiohttp


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self,):
        print(F'fun is ready')
        print("---")


    @commands.command()
    async def echo(self, ctx):
        embed = discord.Embed(title="send your text", description="1min")
        sent = await ctx.send(embed=embed)


        try:
            msg = await self.client.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel)
            if msg:
                await sent.delete()
                await msg.delete()
                await ctx.send(msg.content)

        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Chancelling due to timeout.", delete_after=10)

    @commands.command()
    async def coinflip(self, ctx):
        embed = discord.Embed(title="Kopf oder Zahl ?")
        sent = await ctx.send(embed=embed)

        try:
            msg = await self.client.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel)
            if msg:
                msg_content = msg.content
                zufall_ls = ["Head", "Number"]
                ergebnis = random.choice(zufall_ls)


                if msg_content == "Head":
                    if ergebnis == "Head":
                        await ctx.send("Its `Head` you won Nice!")


                elif msg_content == "Number":
                    if ergebnis == "Number":
                        await ctx.send("Its `Number` you won Nice!")

                else:
                    await ctx.send("Pleae only `Head` or `Number`")



        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Chancelling due to timeout.", delete_after=10)

    @commands.command()
    async def wikipedia(self, ctx):
        search = ctx.message.content
        definition = wikipedia.summary(search, sentences=3, chars=1000, auto_suggest=True, redirect=True)
        print(search)
        searcheb = discord.Embed(title="Wikipedia", description=definition, color=0xfcfcfc)
        searcheb.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/788451083890327554/800542628118659072/1200px-Wikipedia-logo-v2-simple.svg.png")

        await ctx.send(embed=searcheb)


    @commands.command()
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                 async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    cateb = discord.Embed(title="Random Cat image", color=0xfcfcfc)
                    cateb.set_image(url=data['file'])
                    cateb.set_footer(text="http://random.cat")
                    await ctx.send(embed=cateb)


    @commands.command()
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    dogeb = discord.Embed(title="Random Dog image", color=0xfcfcfc)
                    dogeb.set_image(url=data['url'])
                    dogeb.set_footer(text="https://random.dog/")
                    await ctx.send(embed=dogeb)

    @commands.command()
    async def meme(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/meme") as r:
                    data = await r.json()

                    memeeb = discord.Embed(title="Random Meme", description=f"Caption \n {data['caption']}", color=0x8c45f7)
                    memeeb.set_image(url=data['image'])
                    await ctx.send(embed=memeeb)

                    
    @commands.command()
    async def trigger(self, ctx, user: discord.Member = None):
        async with ctx.channel.typing():
            if user == None:
                user = ctx.author
                triggereb = discord.Embed(title="test", color=0x8c45f7)
                triggereb.set_image(url=f"https://some-random-api.ml/canvas/triggered/?avatar={user.avatar_url}")
                await ctx.send(embed=triggereb)



    @commands.command()
    async def joke(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/joke") as r:
                    data = await r.json()

                    dadeb = discord.Embed(title="Random Joke", description=f" **Joke:** \n {data['joke']}", color=0x8c45f7)
                    await ctx.send(embed=dadeb)

def setup(client):
    client.add_cog(fun(client))
    