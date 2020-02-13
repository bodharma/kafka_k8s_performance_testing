from kafka.init import KafkaMessenger
import json
import time
import os

KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', "test")
KAFKA_URL = os.environ.get('KAFKA_URL', "kafka:9092")
MESSAGES_PER_SECOND = int(os.environ.get('MESSAGES_PER_SECOND', "5"))

def import_json():
    file_j = open('opt/data.json', 'r')
    json_file = json.load(file_j)
    return json_file


def sleeper(messages_per_second):
    sleep_time = (100/messages_per_second)/100
    print(sleep_time)
    time.sleep(sleep_time)


if __name__ == '__main__':
    producer = KafkaMessenger().init_kafka_producer(KAFKA_URL=KAFKA_URL)
    data = import_json()

    while True:
        start_time = time.time()
        msg = KafkaMessenger().create_json_message(data=data)
        KafkaMessenger().send_message(producer, KAFKA_TOPIC, "test", msg)
        elapsed_time = time.time() - start_time
        sleeper(MESSAGES_PER_SECOND)



