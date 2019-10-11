import googlesearch
from Search import Search
import logging


class SearchImage(Search):
    def search(self, query, number, standard):
        logging.info("Recherche google image : " + query)

        racineURL = 'https://www.google.co.in/search?q={}&start={}&tbm=isch&num={}&filter=0'

        # on s'appuie sur les resultats renvoyé par google search et non ceux de googles images pour de meilleurs résultats
        return googlesearch.search(
            query,
            tld="fr",
            lang="fr",
            num=50,
            start=0,
            stop=int(number),
            pause=2,
            # (tpe = search type) : Use the following values {videos: ‘vid’, images: ‘isch’, news: ‘nws’, shopping: ‘shop’, books: ‘bks’, applications: ‘app’}
            tpe='isch',
            only_standard=(standard == "True"))
