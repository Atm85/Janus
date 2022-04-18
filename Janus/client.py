import discord
from discord import app_commands
from Janus import commands


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
        self.tree.add_command(commands.ping, guild=discord.Object(id="774799324373712907"))

    # called when the bot establishes a connection with discord
    # ---------- Overridden from 'commands.Bot' class ----------
    ############################################################
    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Game(name="Welcome members with style!"))
        await self.tree.sync(guild=discord.Object(id="774799324373712907"))
        print(self.user.name + " - status: online")

    # called when a member join a guild
    ####################################
    async def on_member_join(self, member):

        # gets the members avatar
        if not member.avatar_url == "":
            avatar = member.avatar_url
        else:
            avatar = member.default_avatar_url

        # if guild_id is not found in database, do nothing
        if self.provider.get_guild(member.guild.id) is None:
            return

        # if join message are disabled, do nothing
        if not self.provider.is_enabled(member.guild.id):
            return

        # sends message
        channel = member.guild.get_channel(Janus.provider.get_channel(member.guild.id))
        message = self.provider.format_message(Janus.provider.get_message(member.guild.id), member.guild, member)
        await self.provider.send(channel, message, avatar)

# end of class
