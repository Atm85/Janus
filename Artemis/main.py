from client import Artemis
from provider import MysqlProvider


def main():

    # register data-storing instance
    #################################
    provider = MysqlProvider()

    # create new bot instance
    #################################
    client = Artemis(provider)

    # connect to discord websocket
    #################################
    client.run(provider.token)


if __name__ == '__main__':
    main()
