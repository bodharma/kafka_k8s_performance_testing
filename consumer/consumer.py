import os
import datetime

from confluent_kafka import Consumer, KafkaException
from loguru import logger


KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', "test")
KAFKA_URL = os.environ.get('KAFKA_URL', "kafka:9092")


def init_kafka_consumer(KAFKA_URL):
    """
    used to connect to kafka
    :param KAFKA_URL:
    :return: consumer that is able to get messages from kafka
    """
    conf = {
        'bootstrap.servers': KAFKA_URL,
        'group.id': 'jmsgroup'
    }
    consumer = Consumer(conf)
    logger.info(f"Connected to kafka {KAFKA_URL} - {datetime.datetime.now()}")
    return consumer


consumer = init_kafka_consumer(KAFKA_URL)
consumer.subscribe(topics=[KAFKA_TOPIC])
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            logger.info(f"Received message in TOPIC {msg.topic()} with KEY {msg.key()} - VALUE {msg.value()}")
finally:
    consumer.close()

