import asyncio
import discord

from discord.ext import commands
from client import Artemis


class MessageCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def message(self, ctx):

        # database connection
        connection = Artemis.provider.connection

        # gets a response from the user after executing main command
        def get_response(response):

            # the message received from the response
            content = response.content

            # update query in database
            with connection.cursor() as cursor:

                # create new entry if not existent
                if Artemis.provider.get_guild(ctx.message.guild.id) is None:
                    Artemis.provider.create_new(ctx.message.guild.id)

                # saves message content to database
                Artemis.provider.save_message(ctx.message.guild.id, content)

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
        embed = discord.Embed(
            color=12632256,
            title="message keywords"
        )

        embed.add_field(name="{u}", value="members username")
        embed.add_field(name="{s}", value="servers name")
        embed.add_field(name="{m}", value="mention new user")
        embed.add_field(name="{c}", value="membercount")
        await ctx.message.channel.send("Please send the message you wist to use! time-out in 30s", embed=embed)

        # listen for response, fail on timeout
        try:
            await self.client.wait_for("message", check=get_response, timeout=30.0)
            from_database = Artemis.provider.get_message(ctx.message.guild.id)
            message = Artemis.provider.format_message(from_database, ctx.message.guild, ctx.message.author)
            embed1 = discord.Embed(
                color=12632256,
                title="Message has been set!",
                description=message
            )

            await ctx.message.channel.send(embed=embed1)

        except asyncio.TimeoutError:
            await ctx.message.channel.send("command timed-out! try again")


def setup(client):
    client.add_cog(MessageCommand(client))
