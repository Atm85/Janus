import asyncio

import discord
from discord import app_commands
from Janus import commands


async def update_presence(client: discord.Client):

    while True:

        members = 0
        servers = len(client.guilds)

        for guild in client.guilds:
            members += len(guild.members)

        activity = discord.Activity(name=f"Welcoming {members} members in {servers} servers", type=0)
        await client.change_presence(activity=activity)
        await asyncio.sleep(5)


class Janus(discord.Client):

    # bot prefix
    prefix = None

    # data-store provider
    provider = None

    # initializes the bot client
    ############################################################
    def __init__(self, provider, **options):
        print("starting...")
        super().__init__(intents=discord.Intents().all())
        self.provider = provider
        self.tree = app_commands.CommandTree(self)
        self.tree.add_command(commands.Image())
        self.tree.add_command(commands.channel)
        self.tree.add_command(commands.help)
        self.tree.add_command(commands.info)
        self.tree.add_command(commands.message)
        self.tree.add_command(commands.ping)
        self.tree.add_command(commands.preview)

    # called when the bot establishes a connection with discord
    # ---------- Overridden from 'commands.Bot' class ----------
    ############################################################
    async def on_ready(self):
        await self.wait_until_ready()
        await self.tree.sync()
        print(self.user.name + " - status: online")
        await update_presence(self)

    # called when a member join a guild
    ####################################
    async def on_member_join(self, member: discord.Member):

        # gets the members avatar
        if member.avatar is None:
            avatar = member.default_avatar.url
        else:
            avatar = member.avatar.url

        # if guild_id is not found in database, do nothing
        if self.provider.get_guild(member.guild.id) is None:
            return

        # if join message are disabled, do nothing
        if not self.provider.is_enabled(member.guild.id):
            return

        # sends message
        channel = member.guild.get_channel(self.provider.get_channel(member.guild.id))
        message = self.provider.format_message(self.provider.get_message(member.guild.id), member.guild, member)
        await self.provider.send(channel, message, avatar)

# end of class
