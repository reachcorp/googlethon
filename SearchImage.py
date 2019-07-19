import googlesearch
from Search import Search
import logging


class SearchImage(Search):

    def search(self, query, number, standard):
        logging.info("Recherche google image : " + query)

        return googlesearch.search(
            "jacques chirac rugby",
            tld="fr",
            lang="fr",
            num=50,
            start=0,
            stop=int(number),
            pause=2,
            tpe='isch',
            only_standard=Search.convert(standard))
