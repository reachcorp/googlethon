from selenium import webdriver
import logging
import urllib
from Search import Search
import time
from selenium.webdriver.firefox.options import Options

class SearchNews(Search):

    def modulo_url(self, query, resultPerPage, nbMax):

        encoded_search = urllib.parse.quote(query)
        # TODO valider le domaine google.co.in VERSUS google.fr ou .com....
        racineURL = 'https://www.google.co.in/search?q={}&start={}&num={}&filter=0&tbm=nws'

        tabURL = []
        for i in range(nbMax // resultPerPage):
            tabURL.append(racineURL.format(encoded_search, i * resultPerPage, resultPerPage))

        tabURL.append(
            racineURL.format(encoded_search, (nbMax // resultPerPage) * resultPerPage, (nbMax % resultPerPage)))
        return tabURL

    def search(self, query, number, urlList):
        logging.info("Recherche google news : " + query)

        query = query.replace(' ', '+')
        options = Options()
        options.add_argument('--headless')
        browser = webdriver.Firefox(executable_path=r"./lib/geckodriver", options=options)

        listeUrls = SearchNews.modulo_url(self, query, 50, number)

        # Remonte les URLs de google news, les URLs avec une balise de titre <h3>
        for url_request in listeUrls:
            browser.get(url_request)
            time.sleep(1)

            liste_titres_h3 = browser.find_elements_by_xpath("//div/h3/a")

            for elt in liste_titres_h3:
                current_url = elt.get_attribute("href")
                urlList.append(current_url)

        browser.quit()

