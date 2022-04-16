import discord
from discord.ext import commands

internal_extensions = [
    "Janus.commands.help",
    "Janus.commands.info",
    "Janus.commands.ping",
    "Janus.commands.channel",
    "Janus.commands.message",
    "Janus.commands.image",
    "Janus.commands.test"
]


class Janus(commands.Bot):

    # bot prefix
    prefix = None

    # data-store provider
    provider = None

    # initializes the bot client
    ############################################################
    def __init__(self, provider, **options):
        intents = discord.Intents().default()
        intents.members = True
        super().__init__(provider.prefix, intents=intents)

        self.remove_command("help")
        Janus.prefix = provider.prefix
        Janus.provider = provider
        print("starting...")

    # called when the bot establishes a connection with discord
    # ---------- Overridden from 'commands.Bot' class ----------
    ############################################################
    async def on_ready(self):

        # changes bots presence in discord
        await self.change_presence(activity=discord.Game(name="Bot help | {}help".format(self.prefix)))

        # registers bot commands
        for ext in internal_extensions:
            try:
                self.load_extension(ext)
                print("--> {} has been loaded".format(ext))
            except Exception as error:
                print("[x] {} failed to load: [{}]".format(ext, error))

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
