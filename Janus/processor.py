import aiohttp
import discord
import base64
import requests
import Janus

from io import BytesIO
from PIL import Image, ImageDraw, ImageOps


class Processor:

    def __init__(self):
        pass

    @staticmethod
    def encode(url):
        buffered = BytesIO(requests.get(url).content)
        to_base64 = base64.b64encode(buffered.getvalue())
        return to_base64.decode()

    @staticmethod
    async def upload(channel, message, avatar):

        # denote typing status
        async with channel.typing():

            # open client session
            async with aiohttp.ClientSession() as session:

                # read avatar image data
                async with session.get(str(avatar)) as image:
                    result = await image.read()

                # opens user avatar
                with Image.open(BytesIO(result)) as avatar:

                    # decode banner from base64
                    buffer = BytesIO()
                    base64_string = Janus.provider.get_base64(channel.guild.id)
                    decode_b64 = base64.b64decode(base64_string.decode())
                    bytes_ = BytesIO(decode_b64)
                    banner = Image.open(bytes_)

                    # avatar args
                    pos = Janus.provider.get_avpos(channel.guild.id)
                    avsize = round((banner.height * Janus.provider.get_avsize(channel.guild.id) / 100))

                    # calculate avatar position on the banner
                    if pos == "L":
                        x = (round((banner.height - avsize) / 2) - round(avsize / 2) + round(avsize / 4))
                        y = round((banner.height - avsize) / 2)
                    elif pos == "C":
                        x = round((banner.width - avsize) / 2)
                        y = round((banner.height - avsize) / 2)
                    elif pos == "R":
                        x = (round((banner.height - avsize) / 2) + round(avsize * 2) - round(avsize / 4))
                        y = round((banner.height - avsize) / 2)

                    # generates circular alpha mask
                    avatar = avatar.resize((avsize, avsize))
                    size = (avatar.size[0] * 3, avatar.size[1] * 3)
                    mask = Image.new("L", size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0) + size, fill=255)
                    mask = mask.resize(avatar.size, Image.ANTIALIAS)
                    avatar.putalpha(mask)

                    # generates a white border around the users avatar
                    border = Image.new("L", size, 0)
                    ellipse = ImageDraw.Draw(border)
                    ellipse.ellipse((0, 0) + size, outline=255, width=25)
                    border = border.resize((avsize + 10, avsize + 10))
                    b_mask = mask.resize(border.size, Image.ANTIALIAS)

                    # pastes avatar mask on banner and saves for uploading
                    banner.paste(border, (x - 5, y - 5), b_mask)
                    banner.paste(avatar, (x, y), mask)
                    banner.save(buffer, "png")
                    buffer.seek(0)

                # send processed image to set channel
                file = discord.File(fp=buffer, filename="welcome.png")
                embed = discord.Embed(color=3553599, description=message)
                embed.set_image(url="attachment://welcome.png")
                embed.set_footer(text="joined at position: {}".format(str(len(channel.guild.members))))
                await channel.send(file=file, embed=embed)


# formula for vertical positioning
# - (height - avatar-size) / 2
#
# formula for horizontal positioning
# - (width - avatar-size) / 2
#
# formula for avatar size
# -----------------------------------
# - (height * 50) / 100
#
