from kafka import KafkaProducer
import json
import logging
from time import sleep


def main():
    try:
        logging.basicConfig(level=logging.ERROR)
        #producer = KafkaProducer(bootstrap_servers='localhost:8092')
        producer = KafkaProducer(bootstrap_servers='localhost:8092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        print("bonjour")
        for _ in range(10):
            #producer.send('topicgoogle', b'some_message_bytes')
            producer.send('topicgoogle', value={'nom': 'bar', 'prenom': 'bar', 'idBio': 'bar' })
            sleep(2)
    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin du bouchon ")
        exit(0)

if __name__ == '__main__':
    main()