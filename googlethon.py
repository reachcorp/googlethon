import datetime
import json
import logging
import requests
import urllib.parse
from bs4 import BeautifulSoup
from kafka import KafkaConsumer
from kafka import KafkaProducer

kafka_endpoint = str(os.environ['KAFKA_IP']) + ":" + str(os.environ['KAFKA_PORT'])
number = str(os.environ['NUMBER_RESULT'])
standard = str(os.environ['STANDARD'])
topic_in = str(os.environ['TOPIC_IN'])
topic_out_scrapy = str(os.environ['TOPIC_OUT_SCRAPY'])
debug_level = os.environ["DEBUG"]
search_type = os.environ["SEARCH_TYPE"]

# kafka_endpoint = "192.168.0.9:8092"
# number = 10
# standard = "True"
# topic_in = "housToGoogle"
# topic_out_scrapy = "urlToScrapy"
# debug_level = "INFO"
# # Trois options de recherche Google : SearchImage, SearchUrl, SearchNews
# # search_type est aussi le group_id du consumer kafka
# search_type = "SearchUrl"

def modulo_url (search, resultPerPage, nbMax) :

    #TODO: attention, on rajoute "+2" comme un cochon sinon on a un delta, à investigué quand on aura le temps...
    nbMax +=2

    encoded_search = urllib.parse.quote(search)
    #TODO valider le domaine google.co.in VERSUS google.fr ou .com....
    racineURL = 'https://www.google.co.in/search?q={}&start={}&num={}&filter=0'

    tabURL=[]
    for i in range(nbMax // resultPerPage):
        tabURL.append(racineURL.format(encoded_search, i*resultPerPage, resultPerPage))

    tabURL.append(racineURL.format(encoded_search, (nbMax // resultPerPage)*resultPerPage, (nbMax % resultPerPage)))
    return tabURL

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

            ######################################################################################
            #  Pour chaque url récupéré en fonction du nom et du prénom,
            # search: requete à google
            # search.num :  le nombre de resultat par page
            # search.pause : le nombre de seconde de pause entre chaque page
            # pour ne pas avoir son IP bloqué par Google (si le nombre de requete est trop élevé)
            # search.stop : arret à n°X resultats, None pour chercher sans limite
            # search.only_standard : True -> resultat standard
            #                        False -> tous les liens
            ######################################################################################
            urlList = []

            ########################
            ### ANCIEN CODE
            ########################
            # for j in Search.factory(search_type).search(query, number, standard):
            #     # Envoie l'url + les infos de la personne dans le Topic topicscrapython
            #     logging.debug(j)
            #     urlList.append(j)


            ########################
            ### NOUVEAU CODE
            ########################

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Accept' :
                    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language' : 'fr-fr,en;q=0.5',
                'Accept-Encoding' : 'gzip',
                'DNT' : '1', # Do Not Track Request Header
                'Connection' : 'close'
            }

            listeUrls = modulo_url(query, 50, number)


            #TODO adapter pour fonctionner avec news et images.

            # Remonte les URLs de google search, les URLs avec une balise de titre <h3>
            for i in range(len(listeUrls)):
                resp = requests.get(listeUrls[i], headers=headers).text
                soup = BeautifulSoup(resp, 'html.parser')
                for link in soup.findAll('a', href=True):
                    if (str(link).find("<h3") != -1):
                        urlList.append(link.attrs.get('href'))

            # json a mettre dans la file kafka
            jsonvalue = { 'biographics': {
                "nom": nom,
                "prenom": prenom,
                "idBio": idBio
                },
                "url": urlList,
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
