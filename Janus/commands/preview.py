import discord
from discord import app_commands


@app_commands.command(description="previews welcome message")
async def preview(interaction: discord.Interaction):

    client = interaction.client
    author = interaction.user

    # gets the users avatar url
    if author.avatar is None:
        avatar_url = author.default_avatar.url
    else:
        avatar_url = author.avatar.url

    # if guild_id is not found in database
    if client.provider.get_guild(interaction.guild.id) is None:
        await interaction.response.send_message(content="Welcome messages are not setup for this server!")
        return

    # if join message are disabled, do nothing
    if not client.provider.is_enabled(interaction.guild.id):
        await interaction.response.send_message(content="Welcome messages are not enabled for this server!")
        return

    # args for sending the message
    channel = interaction.channel
    message = client.provider.format_message(client.provider.get_message(interaction.guild.id), interaction.guild, author)
    await interaction.response.send_message("Sending...")
    await client.provider.send(channel, message, avatar_url)
