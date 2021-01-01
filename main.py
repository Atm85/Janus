from Janus import Client
from Janus import MysqlProvider


def main():

    # register data-storing instance
    #################################
    provider = MysqlProvider()

    # create new bot instance
    #################################
    client = Client(provider)

    # connect to discord websocket
    #################################
    client.run(provider.token)


if __name__ == '__main__':
    main()
