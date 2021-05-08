import sys
import csv
from database import Database
from datetime import datetime as dt
import paho.mqtt.client as mqtt

fieldnames = ["date", "mess"]


class Subscriber:
    """Creaetes subscriber for given topic"""

    def __init__(self) -> None:
        self.datbase = Database()
        self.db, self.cursor = self.datbase.return_db_obj()

        self.broker = "127.0.0.1"
        self.port = 1883
        self.topics = self.load_topics()

    def __del__(self):
        self.datbase.close_connection()

    def load_topics(self) -> list:
        topics = []
        query = "select topic from conf"

        self.cursor.execute(query)
        for each in self.cursor:
            topics.append(str(each).strip("('),"))

        return topics

    def read_data(self, msg):
        """Parses recieved data
            Data is recieved as a string with date and value separated
            by comma - that allows to easly split them.

        Parameters
        ----------
        msg : [type]
            msg object recieved from mqtt broker

        Returns
        -------
        str, int
            Values recieved from publisher, first one is date returned as a string,
            second one is value which is passed as int.
        """
        data = msg.payload.decode().strip("()").split(sep=", ")
        date = data[0]
        val = int(data[1])
        return date, val

    # def log(self, msg):
    #     """ Saves recieved data to csv file

    #     Parameters
    #     ----------
    #     msg : [type]
    #         msg object recieved from mqtt broker
    #     """
    #     date, mess = self.read_data()
    #     with open("data.csv", "a") as csv_file:
    #         csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    #         info = {
    #             "date": date,
    #             "mess": mess,
    #         }
    #         csv_writer.writerow(info)

    def save_to_database(self, date, val, topic):
        add_data = ("insert into data (date, id_d, id_c, val) values (%s, %s, %s, %s)")

        ids = topic.split("/")
        date_ = dt.strptime(date.strip("'"), "%Y-%m-%d %H:%M:%S.%f")
        data = (date_, int(ids[0]), int(ids[1]), int(val))

        self.cursor.execute(add_data, data)
        self.db.commit()


    def connect(self) -> mqtt.Client:
        """Connects to MQTT broker

        Returns
        -------
        mqtt.Client
            MQTT client object
        """

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
            date = dt.now().strftime("[%H:%M:%S]")
            date_sent, val = self.read_data(msg)
            print(
                f"{date}: Received `{val}` sent at {date_sent} from {msg.topic} topic"
            )
            self.save_to_database(date_sent, val, msg.topic)

        for topic in self.topics:
            client.subscribe(topic)
            client.on_message = on_message
