import discord
from appuselfbot import isBot
from discord.ext import commands
import asyncio


class Userinfo:

    def __init__(self, bot):
        self.bot = bot

    # Get user info
    @commands.group(pass_context=True)
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            name = ctx.message.content[5:].strip()
            if name:
                try:
                    name = ctx.message.mentions[0]
                except:
                    name = ctx.message.server.get_member_named(name)
                if not name:
                    await self.bot.send_message(ctx.message.channel, isBot + 'Could not find user.')
                    return
            else:
                name = ctx.message.author

            # Thanks to IgneelDxD for help on this
            if name.avatar_url[60:].startswith('a_'):
                avi = 'https://images.discordapp.net/avatars/' + name.avatar_url[33:][:18] + name.avatar_url[59:-3] + 'gif'
            else:
                avi = name.avatar_url

            try:
                perms = ctx.message.author.permissions_in(ctx.message.channel).attach_files and ctx.message.author.permissions_in(ctx.message.channel).embed_links
            except:
                perms = True

            if perms:
                em = discord.Embed(timestamp=ctx.message.timestamp, colour=0x708DD0)
                em.add_field(name='User ID', value=name.id, inline=True)
                em.add_field(name='Nick', value=name.nick, inline=True)
                em.add_field(name='Status', value=name.status, inline=True)
                em.add_field(name='In Voice', value=name.voice_channel, inline=True)
                em.add_field(name='Account Created', value=name.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
                em.add_field(name='Join Date', value=name.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
                em.set_thumbnail(url=avi)
                em.set_author(name=name, icon_url='https://i.imgur.com/RHagTDg.png')
                await self.bot.send_message(ctx.message.channel, embed=em)
            else:
                msg = '**User Info:** ```User ID: %s\nNick: %s\nStatus: %s\nIn Voice: %s\nAccount Created: %s\nJoin Date: %s\nAvatar url:%s```' % (name.id, name.nick, name.status, name.voice_channel, name.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), name.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), avi)
                await self.bot.send_message(ctx.message.channel, isBot + msg)

            await asyncio.sleep(2)
            await self.bot.delete_message(ctx.message)

    @info.command(pass_context=True)
    async def avi(self, ctx):
        name = ctx.message.content[9:].strip()
        if name:
            try:
                name = ctx.message.mentions[0]
            except:
                name = ctx.message.server.get_member_named(name)
            if not name:
                await self.bot.send_message(ctx.message.channel, isBot + 'Could not find user.')
                return
        else:
            name = ctx.message.author

        # Thanks to IgneelDxD for help on this
        if name.avatar_url[60:].startswith('a_'):
            avi = 'https://images.discordapp.net/avatars/' + name.avatar_url[33:][:18] + name.avatar_url[59:-3] + 'gif'
        else:
            avi = name.avatar_url
        try:
            perms = ctx.message.author.permissions_in(ctx.message.channel).attach_files and ctx.message.author.permissions_in(ctx.message.channel).embed_links
        except:
            perms = True
        if perms:
            em = discord.Embed(colour=0x708DD0)
            em.set_image(url=avi)
            await self.bot.send_message(ctx.message.channel, embed=em)
        else:
            await self.bot.send_message(ctx.message.channel, isBot + avi)
        await asyncio.sleep(2)
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Userinfo(bot))