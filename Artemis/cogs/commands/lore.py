import discord
from discord.ext import commands


class LoreCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def lore(self, ctx):

        embed = discord.Embed(
            color=12632256,
            title="Artemis v2.0",
            description="Artemis is the Greek goddess of the hunt, the wilderness, wild animals, the Moon, and chastity. Artemis is the daughter of Zeus and Leto, and the twin sister of Apollo"
        )

        embed.add_field(name="Read more?", value="[from wikipedia.org](https://en.wikipedia.org/wiki/Artemis)")
        await ctx.message.channel.send(embed=embed)


def setup(client):
    client.add_cog(LoreCommand(client))
