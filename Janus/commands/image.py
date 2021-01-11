import asyncio
import Janus

from discord.ext import commands
from Janus import Client


class ImageCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def image(self, ctx):

        # database connection
        connection = Client.provider.connection

        # gets the response from the user after executing main command
        def get_response(response):

            # check if the response contains an attachment
            if response.attachments:

                # encodes the attachments url into base64 binary
                to_base64 = Janus.processor.encode(response.attachments[0].url)

                # save bas64 image data to database
                Client.provider.set_using_image(ctx.message.guild.id, True)
                Client.provider.save_image(ctx.message.guild.id, to_base64)

            # run only if response is sent by the main user
            return response.author == ctx.message.author

        # check user permissions
        if not ctx.message.author.guild_permissions.administrator:

            onward = False

            if ctx.message.author.id == 421043401040068608:
                onward = True

            if not onward:
                await ctx.message.channel.send("You do not have permission to use this command!")
                return

        # continue with setup
        await ctx.message.channel.send("Please upload the image you wish to use... supports images of ANY dimensions! - `command will time-out in 30s`")

        # listen for response, fail on timeout
        try:
            await self.client.wait_for("message", check=get_response, timeout=30.0)
            await ctx.message.channel.send("Image set!, run command '{}test' to preview".format(Client.prefix))
        except asyncio.TimeoutError:
            await ctx.message.channel.send("command timed-out! try again")


def setup(client):
    client.add_cog(ImageCommand(client))
