import datetime
import json
import logging
import os

from kafka import KafkaConsumer
from kafka import KafkaProducer

from Search import Search

kafka_endpoint = str(os.environ['KAFKA_IP']) + ":" + str(os.environ['KAFKA_PORT'])
number = str(os.environ['NUMBER_RESULT'])
topic_in = str(os.environ['TOPIC_IN'])
topic_out_scrapy = str(os.environ['TOPIC_OUT_SCRAPY'])
debug_level = os.environ["DEBUG"]
search_type = os.environ["SEARCH_TYPE"]

# kafka_endpoint = "192.168.0.9:8092"
# number = 183
# topic_in = "housToGoogle"
# topic_out_scrapy = "urlToScrapy"
# debug_level = "DEBUG"
# # Trois options de recherche Google : SearchImage, SearchResult, SearchNews
# # search_type est aussi le group_id du consumer kafka
# search_type = "SearchNews"


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

        logging.info(" Démarrage de Googlethon " + str(datetime.datetime.now()))

        # Recupère les personnes dans la file kafka entre Housthon et Googlethon
        consumer = KafkaConsumer(
            topic_in,
            bootstrap_servers=[kafka_endpoint],
            group_id=search_type,
            auto_offset_reset='earliest',
            value_deserializer=lambda v: json.loads(v.decode('utf-8')))

        # Set un producer
        producer = KafkaProducer(
            bootstrap_servers=[kafka_endpoint],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        # Traite les résultats (personnes) récupérés par le consumer
        for message in consumer:
            message = message.value

            query = message['nom'] + " " + message['prenom']

            if 'motclef' in message:
                query = query + " " + message['motclef']
            logging.info("### Googlethon : reception d'un message ! " + str(datetime.datetime.now()))
            logging.info("### recherche de " + query)
            # recuperation des infos du message du consumer
            nom = message['nom']
            prenom = message['prenom']
            idBio = message['idBio']

            # query : les mots de la requête
            # number :  le nombre de resultats souhaité au total
            # urlList : la liste dans laquelle arriveront les résultats de la requête

            urlList = Search.factory(search_type).search(query, number)
            urlList_to_send = []

            if search_type == "SearchImage":
                urlList_to_send = urlList[:number]
            else:
                urlList_to_send = urlList

            if debug_level == "DEBUG" :
                index = 1
                for url in urlList_to_send:
                    print(str(index) + " : " + url)
                    index += 1

            print("Nombre d'éléments envoyés dans la file Kafka pour une recherche " + search_type + " : " + str(len(urlList_to_send)))

            # Json a mettre dans la file kafka
            jsonvalue = {'biographics': {
                "nom": nom,
                "prenom": prenom,
                "idBio": idBio
            },
                "url": urlList_to_send,
                "idDictionary": message['idDictionary'],
                "depthLevel": message['depthLevel']
            }

            producer.send(
                topic_out_scrapy,
                value=jsonvalue)


    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin de Googlethon ")
        exit(0)


if __name__ == '__main__':
    main()
