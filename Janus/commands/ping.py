import discord, time
from discord import app_commands


@app_commands.command()
async def ping(interaction: discord.Interaction):
    before = time.monotonic()
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(content=f"Pong! `{int((time.monotonic() - before) * 1000)}`")
