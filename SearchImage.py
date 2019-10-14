import logging
import json

from Search import Search


class SearchImage(Search):
    def search(self, query, number):
        logging.info("Recherche Google Images : " + query)
        xpath = "//div[contains(@class,'rg_meta')]"
        return Search.get_urls(self, query, number, xpath)

    def extract_url_from_link(self, link):
        return json.loads(link.get_attribute('innerHTML'))["ru"]
