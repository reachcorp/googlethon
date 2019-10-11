import time
import urllib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

remote_firefox_endpoint = str(os.environ['REMOTE_FIREFOX_IP']) + ":" + str(os.environ['REMOTE_FIREFOX_PORT'])

class Search():
    def search(self, query, number, standard):
        return

    def factory(type):
        if type == "SearchNews":
            from SearchNews import SearchNews
            return SearchNews()
        if type == "SearchImage":
            from SearchImage import SearchImage
            return SearchImage()
        if type == "SearchResult":
            from SearchResult import SearchResult
            return SearchResult()
        assert 0, "Bad shape creation: " + type

    factory = staticmethod(factory)

    def modulo_url(self, query, nbMax, resultPerPage=50):

        encoded_search = urllib.parse.quote(query)

        type_of_search = self.__class__.__name__

        racineURL = ''
        if type_of_search == "SearchNews":
            racineURL = 'https://www.google.co.in/search?q={}&start={}&num={}&filter=0&tbm=nws'
        elif type_of_search == "SearchImage": #TODO : ATTENTION, le parametre "num" ne fonctionne pas avec Google IMAGE!!!!
            racineURL = 'https://www.google.co.in/search?q={}&start={}&num={}&filter=0&tbm=isch'
        elif type_of_search == "SearchResult":
            racineURL = 'https://www.google.co.in/search?q={}&start={}&num={}&filter=0'
        else:
            return []

        tabURL = []
        for i in range(nbMax // resultPerPage):
            tabURL.append(racineURL.format(encoded_search, i * resultPerPage, resultPerPage))

        if (nbMax % resultPerPage) != 0:
            tabURL.append(
                racineURL.format(encoded_search, (nbMax // resultPerPage) * resultPerPage, (nbMax % resultPerPage)))
        return tabURL

    def get_urls(self, query, number, xpath):
        query = query.replace(' ', '+')
        # options = Options()
        # options.add_argument('--headless')
        # browser = webdriver.Firefox(executable_path=r"./lib/geckodriver", options=options)

        browser = webdriver.Remote(
            command_executor="http://"+remote_firefox_endpoint+"/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX)

        listeUrls = Search.modulo_url(self, query, int(number))

        # Remonte les URLs de google news, les URLs avec une balise de titre <h3>
        url_list = []
        for url_request in listeUrls:
            browser.get(url_request)
            time.sleep(1)

            array_of_links = browser.find_elements_by_xpath(xpath)

            for link in array_of_links:
                current_url = self.extract_url_from_link(link)
                url_list.append(current_url)

        browser.quit()

        return url_list
