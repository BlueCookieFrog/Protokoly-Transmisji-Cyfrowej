import sys
import time
import json
import paho.mqtt.client as mqtt
from random import randint
from datetime import datetime as dt


class Topics:
    def __init__(self) -> None:
        try:
            # try to open file and load it
            with open("data/publishers.json", "r") as f:
                self.data = json.load(f)
        except IOError:
            # if file does not exist create it
            with open("data/publishers.json", "w+") as f:
                json.dump({}, f, indent=4)
            # create dictionary
            self.data = {}

    def _save(self) -> None:
        try:
            with open("data/publisher.json", "w+") as f:
                json.dump(self.data, f, indent=4)
        except IOError:
            print("Unexpected error while saving data")

    def _get_data(self) -> dict:
        """Gets topics and channels from user

        Returns
        -------
        dict
            Dictionary of keys with values
        """
        topic = {}
        key = input("Give topic name (Type EOT to finish writing data): ")
        while str(key) != "EOT":
            channels = input(
                "Give channels names separated with commas (leave empty if you want to publish directly to the topic): "
            )
            channels.split(sep=",")
            topic.update({key: channels})

            key = input("Give topic name (Type EOT to finish writing data): ")
        return topic

    def _get_del(self) -> list:
        """Gets Topics that will be deleted

        Returns
        -------
        list
            List of topics
        """
        keys = []
        while True:
            key = input("Give topic name to delete: ")
            keys.append(key.split(sep=","))
            if str(key) != "EOT":
                break
        return keys

    def create(self) -> None:
        """Creates new dataset"""
        topic = self._get_data()
        self.data = topic
        self._save()

    def read(self) -> dict:
        """Returns current data

        Returns
        -------
        dict
            Dictionary of topics and channels
        """
        return self.data

    def update(self, topic=_get_data) -> None:
        self.data.update(topic)
        self._save()

    # def delete(self, keys=_get_del()):
    #     for every in keys:
    #         try:
    #             del self.data[every]
    #         except IndexError:
    #             print(f"Skipped deleting {every}, key does not exist")
    #     self._save()


def read_data(val_range) -> int:
    """Generates random int

    Parameters
    ----------
    val_range : list
        range for generating random int

    Returns
    -------
    int
        random value
    """
    return (
        dt.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        randint(int(val_range[0]), int(val_range[1])),
    )


class Publisher:
    def __init__(self, topic_id, val_range: list) -> None:
        self.data = str(read_data(val_range))
        self.broker = "127.0.0.1"
        self.port = 1883
        self.topic = topic_id

    def connect(self) -> mqtt.Client:
        client = mqtt.Client()
        client.connect(self.broker, self.port)
        return client

    def publish(self, client: mqtt.Client) -> None:
        client.publish(f"{self.topic}", self.data)


def get_topics():
    with open("config/pub.json", "r") as f:
        dict = json.load(f)

    topics = []
    for j in dict[sys.argv[1]]:
        topics.append(f"{sys.argv[1]}/{j}")
    return topics


def run():
    for each in get_topics():
        pub = Publisher(each, (0, 1024))
        client = pub.connect()
        pub.publish(client)


if __name__ == "__main__":

    for _ in range(20):
        run()
        time.sleep(1)
