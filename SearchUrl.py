import googlesearch
from Search import Search
import logging
import urllib
import requests
from bs4 import BeautifulSoup


class SearchUrl(Search):
    def modulo_url(self, query, resultPerPage, nbMax):

        # TODO: attention, on rajoute "+2" comme un cochon sinon on a un delta, à investiguer quand on aura le temps...
        nbMax += 2

        encoded_search = urllib.parse.quote(query)
        # TODO valider le domaine google.co.in VERSUS google.fr ou .com....
        racineURL = 'https://www.google.co.in/search?q={}&start={}&num={}&filter=0'

        tabURL = []
        for i in range(nbMax // resultPerPage):
            tabURL.append(racineURL.format(encoded_search, i * resultPerPage, resultPerPage))

        tabURL.append(
            racineURL.format(encoded_search, (nbMax // resultPerPage) * resultPerPage, (nbMax % resultPerPage)))
        return tabURL

    def search(self, query, number, urlList):
        logging.info("Recherche google url : " + query)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-fr,en;q=0.5',
            'Accept-Encoding': 'gzip',
            'DNT': '1',  # Do Not Track Request Header
            'Connection': 'close'
        }

        listeUrls = SearchUrl.modulo_url(self, query, 50, number)

        # TODO adapter pour fonctionner avec news et images.

        # Remonte les URLs de google search, les URLs avec une balise de titre <h3>
        for i in range(len(listeUrls)):
            resp = requests.get(listeUrls[i], headers=headers).text
            soup = BeautifulSoup(resp, 'html.parser')
            for link in soup.findAll('a', href=True):
                if (str(link).find("<h3") != -1):
                    urlList.append(link.attrs.get('href'))

        return urlList
