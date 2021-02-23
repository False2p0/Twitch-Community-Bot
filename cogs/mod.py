import discord
from discord.ext import commands
import asyncio
import datetime
import time
import os

import pymongo

from pymongo import MongoClient

cluster = MongoClient("") # Mongo DB settings for Warn sys
Warns = cluster[""][""]


class mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mod is ready')
        print("---")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=0):
        await ctx.send(F"Es werden {amount} Nachrichten gelöscht")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=amount + 2)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setdelay(self,ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.message.delete()
        embed = discord.Embed(title="\n", description=f"New slowmode for {seconds}sec", color=discord.colour.Color.dark_blue())
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        embed = discord.Embed(title="\n", color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=F"User info about {member}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Nickname:", value=member.display_name)
        embed.add_field(name="createt at:", value=member.created_at)
        embed.add_field(name="Joind at:", value=member.joined_at)
        embed.add_field(name=f"roles ({len(roles)}):", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Bot ?:", value=member.bot)

        await ctx.send(embed=embed)
        
    @commands.command()
    async def PB(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        PB_eb = discord.Embed(title="Profil Picture", color=0xfcfcfc, timestamp=datetime.datetime.utcnow())
        PB_eb.set_image(url=member.avatar_url)
        await ctx.send(embed=PB_eb)
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self,ctx, member: discord.User, reasons=None):
        if member == None or member == ctx.message.author:
            await ctx.send("You cannot ban yourself")
            return
        if reasons == None:
            await ctx.send(f"You cannot ban {member.mention} without an reason")
            return
        message = discord.Embed(title=f"You have been banned from {ctx.guild.name} for {reasons}", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await member.send(embed=message)
        await ctx.guild.ban(member, reason=reasons)
        await ctx.send(F"{member.name} is banned for {reasons} !")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *,member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entery in banned_users:
            user = ban_entery.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f" You unban `{user.name}#{user.discriminator}`")
                return


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self,ctx, member: discord.User, reasons=None):
        if member == None or member == ctx.message.author:
            await ctx.send("You cannot kick yourself")
            return
        if reasons == None:
            await ctx.send(f"You cannot kick {member.mention} without an reason")
            return
        message = discord.Embed(title=f"You have been kicked from {ctx.guild.name} for {reasons}", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await member.send(embed=message)
        await ctx.guild.ban(member, reason=reasons)
        await ctx.send(F"{member.name} is kicked for {reasons} !")



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.User, *,reason=None):
        if member == None or member == ctx.message.author:
            await ctx.send("You cannot warn yourself")
            return
        elif  reason == None:
            await ctx.send(f"You cannot warn {member.mention} without an reason")
            return
        else:
            await ctx.send(f"You warn `{member.display_name}` for `{reason}` ")
            stats = Warns.find_one({"id": member.id})
            if stats is None:
                newwarn = {"id": member.id, "warns": 1, "reasons": reason}
                Warns.insert_one(newwarn)
            else:
                pluswarn = stats["warns"] + 1
                plusreason = stats["reasons"] + f" | {reason}"
                Warns.update_one({"id": member.id}, {"$set":{"warns": pluswarn, "reasons": plusreason}})

    @commands.command()
    async def warnings(self, ctx, member: discord.User=None):
        member = ctx.author if not member else member
        stats = Warns.find_one({"id": member.id})
        if stats is None:
            embed = discord.Embed(title=f"{member.display_name} dont have any Warnings",color=0xc93c3d)
            await ctx.send(embed=embed)
        else:
            all_warns = stats["warns"]
            all_reasons = stats["reasons"]
            embed = discord.Embed(title=f"Warnings of {member.display_name}", description=f"All Warns of the user: `{all_warns}` \n All Reasons of the Warns: `{all_reasons}` ",color=0xc93c3d)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)


                


def setup(client):
    client.add_cog(mod(client))