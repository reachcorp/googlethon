import os
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import logging
from googlesearch import search


kafka_endpoint = str(os.environ['KAFKA_IP']) + ":" + str(os.environ['KAFKA_PORT'])
number = str(os.environ['NUMBER_RESULT'])
standard = str(os.environ['STANDARD'])
topic_in=str(os.environ['TOPIC_IN'])
topic_out_scrapy=str(os.environ['TOPIC_OUT_SCRAPY'])
debug_level=os.environ["DEBUG"]

def convert(s):
    if s == "True": return True;
    return False

def main():
    try:
        logging.basicConfig(level=logging.INFO)
        if debug_level == "DEBUG":
            logging.basicConfig(level=logging.DEBUG)
        elif debug_level == "INFO":
            logging.basicConfig(level=logging.INFO)
        elif debug_level == "WARNING":
            logging.basicConfig(level=logging.WARNING)
        elif debug_level == "ERROR":
            logging.basicConfig(level=logging.ERROR)
        elif debug_level == "CRITICAL":
            logging.basicConfig(level=logging.CRITICAL)

        logging.info(" Démarrage de Googlethon ")

        # Recupère les personnes dans la file kafka entre Housthon et Googlethon
        consumer = KafkaConsumer(
            topic_in,
            bootstrap_servers=[kafka_endpoint],
            group_id='googlethon',
            auto_offset_reset='latest',
            value_deserializer=lambda v: json.loads(v.decode('utf-8')))

        # Set un producer
        producer = KafkaProducer(
            bootstrap_servers=[kafka_endpoint],
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
            # search.only_standard : True -> resultat standard
            #                        False -> tous les liens
            urlList=[]
            for j in search(
                    query,
                    tld="fr",
                    lang="fr",
                    num=50,
                    start=0,
                    stop=int(number),
                    pause=2,
                    only_standard=convert(standard)):
                # Envoie l'url + les infos de la personne dans le Topic topicscrapython
                logging.debug(j)
                urlList.append(j)
            producer.send(
                topic_out_scrapy,
                value={'url': urlList, 'nom': message['nom'], 'prenom': message['prenom'], 'idBio': message['idBio'] })
    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin de Googlethon ")
        exit(0)

if __name__ == '__main__':
    main()