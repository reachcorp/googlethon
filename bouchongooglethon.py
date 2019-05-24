from kafka import KafkaProducer
import json
import logging
from time import sleep

from argparse import ArgumentParser

parser = ArgumentParser(description='Bouchon googlethon')

parser.add_argument("-v", "--verbosity", action="store_true", help="show debug logs")

options = parser.parse_args()


def main():
    try:
        logging.basicConfig(level=logging.INFO)
        if options.verbosity:
            logging.getLogger().setLevel(logging.DEBUG)

        logging.info(" Démarrage du bouchon ")

        producer = KafkaProducer(bootstrap_servers='localhost:8092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        tab=[
            #{'nom': 'Jouy', 'prenom': 'Bob', 'idBio': '0001' }
            #,
            {'nom': 'Trump', 'prenom': 'Donald', 'idBio': '0002' }
        ]
        for i in range(len(tab)):
            producer.send('topicgoogle', value=tab[i])
            sleep(0.5)

    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin du bouchon ")
        exit(0)

if __name__ == '__main__':
    main()