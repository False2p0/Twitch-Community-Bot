import discord
from discord.ext import commands
import asyncio
import datetime
import time
import os

class admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin is ready')
        print("---")

    # command
    @commands.command(aliases=["ann", "announcement", "a"])
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Please send your Channel id for your announcement")
        embed_send = await ctx.send(embed=embed)

        try:
            msg = await self.client.wait_for(
                "message",
                timeout=300,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel)
            if msg:
                channel_id = msg.content
                message_em = discord.Embed(title="Please send your Announcement")
                message_em.add_field(name="Channel id:", value=channel_id)
                await embed_send.edit(embed=message_em)
                await msg.delete()

            msg2 = await self.client.wait_for(
                "message",
                timeout=300,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel)
            if msg2:
                announce = msg2.content
                end_em = discord.Embed(title="Please send your Announcement", description=announce)
                end_em.add_field(name="Channel id:", value=channel_id)
                await embed_send.edit(embed=end_em)
                await msg2.delete()
                ann_em = discord.Embed(title="\n", description=announce, color=0x8c45f7, timestamp=datetime.datetime.utcnow())
                ann_em.set_thumbnail(url=ctx.guild.icon_url)
                ann_em.set_footer(text="Twitch Community", icon_url=ctx.guild.icon_url)
                await self.client.get_channel(int(channel_id)).send(embed=ann_em)


        except asyncio.TimeoutError:
            await embed_send.delete()
            await ctx.send("Chancelling due to timeout.", delete_after=10)

    @commands.command(aliases=["i", "picture"])
    @commands.has_permissions(administrator=True)
    async def image(self,ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Please send the image Link")
        text = await ctx.send(embed=embed)
        try:
            msg = await self.client.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel)
            if msg:
                img = msg.content
                await text.delete()
                await msg.delete()
                img_eb = discord.Embed(title="\n", color=0x8c45f7)
                img_eb.set_image(url=img)
                await ctx.send(embed=img_eb)

        except asyncio.TimeoutError:
            await text.delete()
            await ctx.send("Chancelling due to timeout.", delete_after=10)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def edit(self,ctx):

        sent_eb = discord.Embed(title="Please send the message id")
        sent = await ctx.send(embed=sent_eb)
        try:
            msg0 = await self.client.wait_for(
                "message",
                timeout=300,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel)
            if msg0:

                msg_id = msg0.content
                await msg0.delete()
                edit_embed = discord.Embed(title="Please enter your Text")
                await sent.edit(embed=edit_embed)


            msg = await self.client.wait_for(
                "message",
                timeout=300,
                check=lambda message: message.author == ctx.author
                                      and message.channel == ctx.channel)
            if msg:
                msg_content = msg.content
                channel = ctx.channel
                ann_em = discord.Embed(title="\n", description=msg_content, color=0x8c45f7,
                                       timestamp=datetime.datetime.utcnow())
                ann_em.set_thumbnail(url=ctx.guild.icon_url)
                ann_em.set_footer(text="temQ eSports", icon_url=ctx.guild.icon_url)
                msg_edit = await channel.fetch_message(msg_id)
                await msg_edit.edit(embed=ann_em)
                await sent.delete()
                await msg.delete()
                await ctx.message.delete()

        except asyncio.TimeoutError:
            await ctx.send("Chancelling due to timeout.", delete_after=10)


def setup(client):
    client.add_cog(admin(client))