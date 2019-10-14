import logging

from Search import Search


class SearchResult(Search):
    def search(self, query, number):
        logging.info("Recherche Google Results : " + query)
        xpath = "//div[@class='rc']/div[@class='r']/a/h3"
        return Search.get_urls(self, query, number, xpath)

    def extract_url_from_link(self, link):
        return link.find_elements_by_xpath("..")[0].get_attribute("href")
