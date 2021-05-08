import sys
import csv
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as Animation
import paho.mqtt.client as mqtt

fieldnames = ["date", "mess"]


class Subscriber:
    def __init__(self, topic_id) -> None:
        self.broker = "127.0.0.1"
        self.port = 1883
        self.topic = f"topic/test/{topic_id}"

    def read_data(self, msg):
        data = msg.payload.decode().split(sep=", ")
        date = data[0]
        val = int(data[1])
        return date, val

    def log(self, msg, date):
        date = dt.now().strftime("%H:%M:%S")
        mess = msg.payload.decode()
        with open("data.csv", "a") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "date": date,
                "mess": mess,
            }
            csv_writer.writerow(info)

    def connect(self) -> mqtt.Client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Successfully connected")
            else:
                print(f"Error {rc}")

        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def subscribe(self, client: mqtt) -> None:
        def on_message(client, userdata, msg):
            date = dt.now().strftime("[%d.%m.%Y, %H:%M:%S]")
            date_sent, val = self.read_data(msg)
            print(
                f"{date}: Received `{val}` sent at {date_sent} from {msg.topic} topic"
            )
            self.log(msg, date)

        client.subscribe(self.topic)
        client.on_message = on_message


def menu() -> Subscriber:

    topic_id = int(input("Write id of topic that you want to subscribe: "))
    if topic_id >= 1:
        return Subscriber(topic_id)
    else:
        raise ValueError


def main():
    try:
        subscriber = menu()
    except ValueError:
        print("Topic id should be integer with values >= 1")
        sys.exit()

    with open("data.csv", "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    client = subscriber.connect()
    subscriber.subscribe(client)
    client.loop_forever()


if __name__ == "__main__":

    main()
