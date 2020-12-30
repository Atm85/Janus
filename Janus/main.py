from client import Janus
from provider import MysqlProvider


def main():

    # register data-storing instance
    #################################
    provider = MysqlProvider()

    # create new bot instance
    #################################
    client = Janus(provider)

    # connect to discord websocket
    #################################
    client.run(provider.token)


if __name__ == '__main__':
    main()