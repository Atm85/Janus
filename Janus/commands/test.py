from discord.ext import commands
from Janus import Client


class TestCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def test(self, ctx):

        # database connection
        connection = Client.provider.connection

        # gets the users avatar url
        if not ctx.message.author.avatar_url == "":
            avatar = ctx.message.author.avatar_url
        else:
            avatar = ctx.message.author.default_avatar_url

        await ctx.message.channel.send("A test message was sent to the channel that was set!")

        # if guild_id is not found in database
        if Client.provider.get_guild(ctx.message.guild.id) is None:
            await ctx.message.channel.send("Welcome messages are not setup for this server!")
            return

        # if join message are disabled, do nothing
        if not Client.provider.is_enabled(ctx.message.guild.id):
            await ctx.message.channel.send("Welcome messages are not enabled for this server!")
            return

        # args for sending the message
        channel = ctx.message.guild.get_channel(Client.provider.get_channel(ctx.message.guild.id))
        message = Client.provider.format_message(Client.provider.get_message(ctx.message.guild.id), ctx.message.guild, ctx.message.author)
        await Client.provider.send(channel, message, avatar)


def setup(client):
    client.add_cog(TestCommand(client))
