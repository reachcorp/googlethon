from kafka import KafkaConsumer
import json
import logging
from kafka import TopicPartition


def main():
    try:
        logging.basicConfig(level=logging.ERROR)
        #consumer = KafkaConsumer('topicgoogle',bootstrap_servers='localhost:8092')
        consumer = KafkaConsumer(
            'topicgoogle',
            bootstrap_servers='localhost:8092',
            auto_offset_reset='smallest',
            value_deserializer=lambda v: json.loads(v.decode('utf-8')))
        # consumer.assign([TopicPartition('topicgoogle', 2)])
        # msg = next(consumer)
        # print(msg)
        for message in consumer:
            message = message.value
            print(message)

    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin de Googlethon ")
        exit(0)

if __name__ == '__main__':
    main()