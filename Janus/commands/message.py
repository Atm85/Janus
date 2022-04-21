import discord
from discord import app_commands


@app_commands.command(description="Sets the global welcome message.")
@app_commands.describe(string="params: {u} => username, {s} => server-name, {m} => mention-user, {c} membercount")
async def message(interaction: discord.Interaction, string: str):

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

    # saves message content to database
    client.provider.save_message(guild.id, string)
    await interaction.response.send_message(embed=discord.Embed(
        color=12632256,
        title="Message has been set!",
        description=client.provider.format_message(string, guild, author)
    ))
