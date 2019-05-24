from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import logging
from googlesearch import search
from argparse import ArgumentParser
from time import sleep

parser = ArgumentParser(description='Retrieving Google URL python script')

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

        # Recupère les personnes dans la file kafka entre Housthon et Googlethon
        consumer = KafkaConsumer(
            'topicgoogle',
            bootstrap_servers='localhost:8092',
            group_id='googlethon',
            auto_offset_reset='earliest',
            value_deserializer=lambda v: json.loads(v.decode('utf-8')))

        # Set un producer
        producer = KafkaProducer(
            bootstrap_servers='localhost:8092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        # Traite les résultats (personnes) récupérés par le consumer
        for message in consumer:
            message = message.value
            query = message['nom'] +" "+message['prenom']
            print("### Googlethon : reception d'un message ! ")
            print("### recherche de "+query)
            # Pour chaque url récupéré en fonction du nom et du prénom,
            annulaire = 0
            # search: requete à google
            # search.num :  le nombre de resultat par page
            # search.pause : le nombre de seconde de pause entre chaque page
            # pour ne pas avoir son IP bloqué par Google (si le nombre de requete est trop élevé)
            # search.stop : arret à n°X resultats, None pour chercher sans limite
            # search.only_standard : true -> resultat standard
            #                        false -> tous les liens
            for j in search(
                    query,
                    tld="fr",
                    lang="fr",
                    num=50,
                    start=0,
                    stop=int(options.number),
                    pause=2,
                    only_standard=True):
                annulaire += 1
                # Envoie l'url + les infos de la personne dans le Topic topicscrapython
                producer.send(
                    'topicscrapython',
                    value={'indice':annulaire, 'url': j, 'nom': message['nom'], 'prenom': message['prenom'], 'idBio': message['idBio'] })
                logging.debug(j)

    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin de Googlethon ")
        exit(0)

if __name__ == '__main__':
    main()