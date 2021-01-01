import discord
import json
import pymysql.cursors

import Janus


def check_data(data) -> bool:
    value = True

    if data["token"] == "":
        value = False

    if data["prefix"] == "":
        value = False

    if data["host"] == "":
        value = False

    if data["user"] == "":
        value = False

    if data["password"] == "":
        value = False

    if data["schema"] == "":
        value = False

    return value


class MysqlProvider:

    token = ""
    prefix = ""
    host = ""
    user = ""
    password = ""
    schema = ""

    connection = None

    def __init__(self):
        try:

            # read data from configuration file
            ####################################
            with open("config.json", 'r') as f:
                data = json.load(f)
                if not check_data(data):
                    print("All fields in config.json must be filled!")
                    exit(1)

                self.token = data["token"]
                self.prefix = data["prefix"]
                self.host = data["host"]
                self.user = data["user"]
                self.password = data["password"]
                self.schema = data["schema"]

        except FileNotFoundError:

            # save new blank config
            ####################################
            with open("config.json", 'w+') as f:
                data = {
                    "token": "",
                    "prefix": "",
                    "host": "",
                    "user": "",
                    "password": "",
                    "schema": "",
                }

                json.dump(data, f, indent=4)
                print("A new blank config file has been generated!")
                print("Please edit configuration file in full and run again...")
                exit(0)

        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.schema)
        try:
            # registers new tables if not existent
            ########################################
            with self.connection.cursor() as cursor:
                sql1 = "CREATE TABLE IF NOT EXISTS guild_data(id BIGINT NOT NULL PRIMARY KEY, channel BIGINT NOT NULL, message TEXT NOT NULL, enabled BOOLEAN NOT NULL)"
                sql2 = "CREATE TABLE IF NOT EXISTS image_data(id BIGINT NOT NULL PRIMARY KEY, base64 MEDIUMBLOB NOT NULL, pos VARCHAR(1) NOT NULL, size TINYINT NOT NULL , use_image BOOLEAN NOT NULL)"
                cursor.execute(sql1)
                cursor.execute(sql2)
                self.connection.commit()

        finally:
            pass
            # self.connection.close()

    def set_using_image(self, guild_id, state):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "UPDATE `image_data` SET `use_image`=%s WHERE `id`=%s"
            cursor.execute(sql, (state, guild_id))
            self.connection.commit()

    def set_enabled(self, guild_id, state):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "UPDATE `guild_data` SET `enabled`=%s WHERE `id`=%s"
            cursor.execute(sql, (state, guild_id))
            self.connection.commit()

    """
    Creates a new database entry
    """
    def create_new(self, id_):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql1 = "INSERT INTO `guild_data` (`id`, `channel`, `message`, `enabled`) VALUES (%s, %s, %s, %s)"
            sql2 = "INSERT INTO `image_data` (`id`, `base64`, `pos`, `size`, `use_image`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql1, (id_, 0, "not set", True))
            cursor.execute(sql2, (id_, "base64", "C", 50, False))
            self.connection.commit()

    """
    Saves the given channel_id to the database
    """
    def save_channel(self, guild_id, channel_id):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "UPDATE `guild_data` SET `channel`=%s WHERE `id`=%s"
            cursor.execute(sql, (channel_id, guild_id))
            self.connection.commit()

    """
    Saves the given message content to the database
    """
    def save_message(self, guild_id, content):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "UPDATE `guild_data` SET `message`=%s WHERE `id`=%s"
            cursor.execute(sql, (content, guild_id))
            self.connection.commit()

    """
    Saves the image from base64 to the database
    """
    def save_image(self, guild_id, base64):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "UPDATE `image_data` SET `base64`=%s WHERE `id`=%s"
            cursor.execute(sql, (base64, guild_id))
            self.connection.commit()

    """
    Gets the guild from the database
    """
    def get_guild(self, id_):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "SELECT * FROM `guild_data` WHERE `id`=%s"
            cursor.execute(sql, id_)
            result = cursor.fetchone()
            return result

    """
    Gets the channel_id from the database
    """
    def get_channel(self, id_):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "SELECT `channel` FROM `guild_data` WHERE `id`=%s"
            cursor.execute(sql, id_)
            result = cursor.fetchone()
            return result[0]

    """
    Gets the message content from the database
    """
    def get_message(self, id_):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "SELECT `message` FROM `guild_data` WHERE `id`=%s"
            cursor.execute(sql, id_)
            result = cursor.fetchone()
            return result[0]

    """
    Gets the base64 encoded image from database
    """
    def get_base64(self, id_):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "SELECT `base64` FROM `image_data` WHERE `id`=%s"
            cursor.execute(sql, id_)
            result = cursor.fetchone()
            return result[0]

    """
    Gets the size of the avatar
    """
    def get_avsize(self, id_):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "SELECT `size` FROM `image_data` WHERE `id`=%s"
            cursor.execute(sql, id_)
            result = cursor.fetchone()
            return result[0]

    """
    Gets the position of the avatar
    """
    def get_avpos(self, id_):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "SELECT `pos` FROM `image_data` WHERE `id`=%s"
            cursor.execute(sql, id_)
            result = cursor.fetchone()
            return result[0]

    """
    returns weather the guild is using an image
    """
    def using_image(self, id_):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "SELECT `use_image` FROM `image_data` WHERE `id`=%s"
            cursor.execute(sql, id_)
            result = cursor.fetchone()
            return result[0]

    def is_enabled(self, id_):
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            sql = "SELECT `enabled` FROM `guild_data` WHERE `id`=%s"
            cursor.execute(sql, id_)
            result = cursor.fetchone()
            return result[0]

    """
    Send the message content to the set channel
    """
    async def send(self, channel, message, avatar):

        # runs is no image is set
        if not self.using_image(channel.guild.id):
            membercount = str(len(channel.guild.members))
            embed = discord.Embed(color=12632256, description=message)
            embed.set_footer(icon_url=avatar, text="Joined at position: {}".format(membercount))
            await channel.send(embed=embed)
            return

        # continue if this guild is using images
        await Janus.processor.upload(channel, message, avatar)

    """
    Formats the message content from the content args
    """
    @staticmethod
    def format_message(message, guild, user):
        return message \
            .replace("{u}", user.name) \
            .replace("{s}", guild.name) \
            .replace("{m}", user.mention)\
            .replace("{c}", str(len(guild.members)))
