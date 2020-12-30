import discord
from discord.ext import commands


class LoreCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def lore(self, ctx):

        embed = discord.Embed(
            color=12632256,
            title="Janus v2.0",
            description="Janus is the Roman god of beginnings, gates, transitions, time, duality, doorways, passages, frames, and endings"
        )

        embed.add_field(name="Read more?", value="[from wikipedia.org](https://en.wikipedia.org/wiki/Janus)")
        await ctx.message.channel.send(embed=embed)


def setup(client):
    client.add_cog(LoreCommand(client))
