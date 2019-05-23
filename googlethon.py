from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import logging
from googlesearch import search
from argparse import ArgumentParser

parser = ArgumentParser(description='OpenALPR Python Test Program')

parser.add_argument("-n", "--number", dest="number", action="store", default="10",
                    help="Number of URL wanted")
parser.add_argument("-v", "--verbosity", action="store_true", help="show debug logs")


options = parser.parse_args()

def main():
    try:
        logging.basicConfig(level=logging.INFO)
        if options.verbosity:
            logging.getLogger().setLevel(logging.DEBUG)

        logging.info(" Démarrage de Googlethon ")

        consumer = KafkaConsumer(
            'topicgoogle',
            bootstrap_servers='localhost:8092',
            group_id='googlethon',
            auto_offset_reset='earliest',
            value_deserializer=lambda v: json.loads(v.decode('utf-8')))

        producer = KafkaProducer(
            bootstrap_servers='localhost:8092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        for message in consumer:
            message = message.value
            query = message['nom'] +" "+message['prenom']
            for j in search(query, tld="co.in", num=int(options.number), stop=int(options.number), pause=2):
                producer.send(
                    'topicscrapython',
                    value={'url': j, 'nom': message['nom'], 'prenom': message['nom'], 'idBio': message['idBio'] })
                logging.debug(j)

    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin de Googlethon ")
        exit(0)

if __name__ == '__main__':
    main()