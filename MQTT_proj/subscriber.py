from subscriber_cls import Subscriber


def main():
    subscriber = Subscriber()

    client = subscriber.connect()
    subscriber.subscribe(client)
    client.loop_forever()


if __name__ == "__main__":

    main()
