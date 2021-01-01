import Janus


def main():

    # create new bot instance
    #################################
    client = Janus.Client(Janus.provider)

    # connect to discord websocket
    #################################
    client.run(Janus.provider.token)


if __name__ == '__main__':
    main()
