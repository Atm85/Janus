import Janus
import discord
from discord import app_commands


class Image(app_commands.Group):

    @app_commands.command(description="Sets an attachment on a welcome message.")
    @app_commands.describe(attachment="The attachment to upload.")
    async def upload(self, interaction: discord.Interaction, attachment: discord.Attachment):

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

        # encodes the attachments url into base64 binary
        base64_encoded = Janus.processor.encode(attachment.url)

        # save bas64 image data to database
        client.provider.set_using_image(guild.id, True)
        client.provider.save_image(guild.id, base64_encoded)
        await interaction.response.send_message("Image set! run command `/preview` to preview settings.")

    @app_commands.command(description="Enables the use of background attachments.")
    async def enable(self, interaction: discord.Interaction):

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

        # save to database
        client.provider.set_using_image(guild.id, True)
        await interaction.response.send_message("Enabled using images.")

    @app_commands.command(description="Disables the use of background attachments.")
    async def disable(self, interaction: discord.Interaction):

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

        # save to database
        client.provider.set_using_image(guild.id, False)
        await interaction.response.send_message("Disabled using images.")
