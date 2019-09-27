import logging
from Search import Search
import datetime


number = 10
standard = "True"

debug_level = "INFO"
# Trois options de recherche Google : SearchImage, SearchUrl, SearchNews
# search_type est aussi le group_id du consumer kafka
search_type = "SearchUrl"


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

         # Traite les résultats (personnes) récupérés par le consumer
        for i in range(100):

            query = "squeezie"

            logging.info("### Googlethon : reception d'un message ! " + str(datetime.datetime.now()))
            logging.info("### recherche de " + query)
            logging.info(i)

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
            for j in Search.factory(search_type).search(query, number, standard):
                # Envoie l'url + les infos de la personne dans le Topic topicscrapython
                logging.debug(j)


    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin de Googlethon ")
        exit(0)


if __name__ == '__main__':
    main()
