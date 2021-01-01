import asyncio

from discord.ext import commands
from Janus import Client


class ChannelCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def channel(self, ctx):

        # database connection
        connection = Client.provider.connection

        # gets the response from the user after executing main command
        def get_response(response):

            # check if the response contains channel mentions
            if response.channel_mentions:

                # strips away special characters from content string
                id_ = response.content.strip("<#>")

                # update query in database
                with connection.cursor() as cursor:

                    # create new entry if not existent
                    if Client.provider.get_guild(ctx.message.guild.id) is None:
                        Client.provider.create_new(ctx.message.guild.id)

                    # saves channel id to database
                    Client.provider.save_channel(ctx.message.guild.id, id_)

                # run only if response is sent by the main user
                return response.author == ctx.message.author

        # check user permissions
        if not ctx.message.author.guild_permissions.administrator:

            onward = False

            if ctx.message.author.id == 287682736104275968:
                onward = True

            if not onward:
                await ctx.message.channel.send("You do not have permission to use this command!")
                return

        # continue with setup
        await ctx.message.channel.send("Please mention the channel you wist to use!")

        # listen for response, fail on timeout
        try:
            await self.client.wait_for("message", check=get_response, timeout=30.0)
            channel = ctx.message.guild.get_channel(Client.provider.get_channel(ctx.message.guild.id))
            await ctx.message.channel.send("{} has been set!".format(channel.mention))
        except asyncio.TimeoutError:
            await ctx.message.channel.send("command timed-out! try again")


def setup(client):
    client.add_cog(ChannelCommand(client))
