import discord
from discord import app_commands


@app_commands.command(description="Displays application help menu.")
async def help(interaction: discord.Interaction):

    author = interaction.user

    # gets the users avatar url
    ##################################
    if author.avatar.url == "":
        icon = author.default_avatar.url
    else:
        icon = author.avatar.url

    # create an embed for the message
    ##################################
    embed = discord.Embed(
        color=12632256,
        title="Application help"
    )

    embed.add_field(name="/channel", value="sets channel to use to send messages in")
    embed.add_field(name="/message", value="sets the join message")
    embed.add_field(name="/image", value="sets the image overlay banner with message (optional)")
    # embed.add_field(name="/pos", value="changes the image overlay position on the banner")
    embed.add_field(name="/info", value="bot information")
    await interaction.response.send_message(embed=embed)
