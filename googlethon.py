import datetime
import json
import logging
import os

from kafka import KafkaConsumer
from kafka import KafkaProducer

from Search import Search


kafka_endpoint = str(os.environ['KAFKA_IP']) + ":" + str(os.environ['KAFKA_PORT'])
topic_in = str(os.environ['TOPIC_IN'])
topic_out_scrapy = str(os.environ['TOPIC_OUT_SCRAPY'])
debug_level = os.environ["DEBUG"]
search_type = os.environ["SEARCH_TYPE"]

# kafka_endpoint = "192.168.0.9:8092"
# topic_in = "housToGoogle"
# topic_out_scrapy = "urlToScrapy"
# debug_level = "DEBUG"
# # Trois options de recherche Google : SearchImage, SearchUrl, SearchNews
# # search_type est aussi le group_id du consumer kafka
# search_type = "SearchResult"


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

        logging.info(" Demarrage de Googlethon " + str(datetime.datetime.now()))

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
            number = int(message['numberUrl'])

            # query : les mots de la requête
            # number :  le nombre de resultats souhaité au total
            # urlList : la liste dans laquelle arriveront les résultats de la requête

            urlList = Search.factory(search_type).search(query, number)

            if search_type == "SearchImage":
                urlList_to_send = urlList[:number]
            else:
                urlList_to_send = urlList

            if debug_level == "DEBUG":
                index = 1
                for url in urlList_to_send:
                    logging.debug(str(index) + " : " + url)
                    index += 1

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
