import googlesearch
from Search import Search
import logging


class SearchUrl(Search):

    def search(self, query, number, standard):
        logging.info("Recherche google url : " + query)

        return googlesearch.search(
            query,
            tld="fr",
            lang="fr",
            num=50,
            start=0,
            stop=int(number),
            pause=2,
            only_standard=(standard == "True"))



