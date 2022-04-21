import discord
from discord import app_commands


@app_commands.command(description="Sets the channel to send messages in.")
@app_commands.describe(channel="The channel to send messages in.")
async def channel(interaction: discord.Interaction, channel: discord.TextChannel):

    client = interaction.client
    author = interaction.user
    guild = interaction.guild

    # check user permissions
    if not author.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command!")
        return

    # create new entry if not exists
    if client.provider.get_guild(guild.id) is None:
        client.provider.create_new(guild.id)

    # saves channel id to database
    client.provider.save_channel(guild.id, channel.id)
    await interaction.response.send_message(content=f"Welcome messages will now be sent in: {channel.mention}")
