import json
import datetime
from confluent_kafka import Producer
from loguru import logger


class KafkaMessenger:

    def init_kafka_producer(self, KAFKA_URL='127.0.0.1:9092'):
        """
        used to connect to kafka
        :param KAFKA_URL:
        :return: producer that is able to send messages to kafka
        """
        conf = {'bootstrap.servers': KAFKA_URL}
        producer = Producer(conf)
        logger.info(f"Connected to kafka {KAFKA_URL} - {datetime.datetime.now()}")
        return producer

    # sender
    def send_message(self, producer, topic, key=None, value=None):
        """
        is used to send message by producer
        :param producer:
        :param topic:
        :param key:
        :param value:
        :return:
        """
        logger.info(f"Sending message - {datetime.datetime.now()}")
        producer.produce(topic, key=key, value=value)

    def create_json_message(self, **kwargs):
        json_data = kwargs['data']
        # TODO: define random values by random generators
        cnvrtd_jsn = json.dumps(json_data)
        return cnvrtd_jsn
