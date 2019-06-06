from kafka import KafkaConsumer
import json
import logging
import time


def main():
    try:
        logging.basicConfig(level=logging.ERROR)
        consumer = KafkaConsumer(
            'urlToScrapy',
            bootstrap_servers='localhost:8092',
            group_id='consumer',
            auto_offset_reset='earliest',
            value_deserializer=lambda v: json.loads(v.decode('utf-8')))
        print(time.time())
        for message in consumer:
            message = message.value
            print(message)

    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        exit(0)

if __name__ == '__main__':
    main()