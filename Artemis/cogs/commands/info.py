import discord
from discord.ext import commands


class InfoCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def info(self, ctx):

        embed = discord.Embed(
            color=12632256,
            title="Artemis v2.0",
            description="Welcome new members with style! overlay new member's avatar over a custom background image. Change the avatars position to fit your needs!"
        )

        embed.add_field(name="Bot author", value="<@287682736104275968>")
        embed.add_field(name="want to add {} to your server?".format(self.client.user), value="[Invite me](https://discord.com/api/oauth2/authorize?client_id=793320535413096448&permissions=8&scope=bot)")
        await ctx.message.channel.send(embed=embed)


def setup(client):
    client.add_cog(InfoCommand(client))
