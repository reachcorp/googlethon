import logging

from Search import Search


class SearchNews(Search):
    def search(self, query, number):
        logging.info("Recherche google news : " + query)
        xpath = "//div/h3/a"
        return Search.get_urls(self, query, number, xpath)

    def extract_url_from_link(self, link):
        return link.get_attribute("href")
