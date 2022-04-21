import discord
from discord import app_commands


@app_commands.command(description="Displays application info.")
async def info(interaction: discord.Interaction):

    embed = discord.Embed(
        color=12632256,
        title="Janus v2.0",
        description="Welcome new members with style! overlay new member's avatar over a custom background image."
    )

    embed.add_field(name="Bot author", value="<@421043401040068608>")
    embed.add_field(name="want to add `Janus#2903` to your server?", value="[Invite me](https://discord.com/api/oauth2/authorize?client_id=793320535413096448&permissions=8&scope=bot)")
    await interaction.response.send_message(embed=embed)
