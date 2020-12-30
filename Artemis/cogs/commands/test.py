import asyncio
import discord

from discord.ext import commands
from client import Artemis


class TestCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def test(self, ctx):

        # database connection
        connection = Artemis.provider.connection

        # gets the users avatar url
        if not ctx.message.author.avatar_url == "":
            avatar = ctx.message.author.avatar_url
        else:
            avatar = ctx.message.author.default_avatar_url

        await ctx.message.channel.send("A test message was sent to the channel that was set!")

        # args for sending the message
        channel = ctx.message.guild.get_channel(Artemis.provider.get_channel(ctx.message.guild.id))
        message = Artemis.provider.format_message(Artemis.provider.get_message(ctx.message.guild.id), ctx.message.guild, ctx.message.author)
        await Artemis.provider.send(channel, message, avatar)


def setup(client):
    client.add_cog(TestCommand(client))
