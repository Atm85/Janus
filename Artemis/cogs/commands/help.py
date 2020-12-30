import discord

from discord.ext import commands
from client import Artemis


class HelpCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Registers help command
    @commands.command(pass_context=True)
    async def help(self, ctx):

        # gets the users avatar url
        ##################################
        if ctx.message.author.avatar_url == "":
            icon = ctx.message.author.default_avatar_url
        else:
            icon = ctx.message.author.avatar_url

        # create an embed for the message
        ##################################
        embed = discord.Embed(
            color=12632256,
            title="{} help".format(self.client.user)
        )

        embed.add_field(name="{}channel".format(Artemis.prefix), value="sets channel to use to send messages in")
        embed.add_field(name="{}message".format(Artemis.prefix), value="sets the join message")
        embed.add_field(name="{}image".format(Artemis.prefix), value="sets the image overlay banner with message (optional)")
        embed.add_field(name="{}pos".format(Artemis.prefix), value="changes the image overlay position on the banner")
        embed.add_field(name="{}info".format(Artemis.prefix), value="bot information")
        embed.add_field(name="{}lore".format(Artemis.prefix), value="Artemis lore")
        embed.add_field(name="{}ping".format(Artemis.prefix), value="view bot latency")

        # sends the discord.Embed to the current channel
        await ctx.message.channel.send(embed=embed)


def setup(client):
    client.add_cog(HelpCommand(client))
