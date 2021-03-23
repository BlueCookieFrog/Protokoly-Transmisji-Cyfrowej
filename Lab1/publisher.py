import sys
import time
import paho.mqtt.client as mqtt
from random import randint


class Publisher:
    def __init__(self, topic_id, val_range: list) -> None:
        self.data = val_range
        self.broker = "127.0.0.1"
        self.port = 1883
        self.topic = f"topic/test/{topic_id}"

    def connect(self) -> mqtt.Client:
        client = mqtt.Client()
        client.connect(self.broker, self.port)
        return client

    def _generate_data(self) -> int:
        return randint(int(self.data[0]), int(self.data[1]))

    def publish(self, client: mqtt.Client) -> None:
        data = self._generate_data()
        client.publish(f"{self.topic}", data)


def run():
    pub = Publisher(sys.argv[1], sys.argv[2:4])
    client = pub.connect()
    pub.publish(client)


if __name__ == "__main__":

    for _ in range(20):
        run()
        time.sleep(1)
