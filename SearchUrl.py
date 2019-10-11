import logging
import time
import urllib

from selenium import webdriver

from Search import Search


class SearchUrl(Search):
    # Crée les requêtes à effectuer successivement
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

    # Execute les requêtes créées par modulo_url et charge urlList avec les url trouvées
    def search(self, query, number, urlList):
        logging.info("Recherche google url : " + query)

        query = query.replace(' ', '+')
        browser = webdriver.Firefox(executable_path=r"./lib/geckodriver")

        listeUrls = SearchUrl.modulo_url(self, query, 50, number)

        # Remonte les URLs de google search, les URLs avec une balise de titre <h3>
        for url_request in listeUrls:
            browser.get(url_request)
            time.sleep(1)

            # Autre méthode pour récupérer les adresses UrL
            # elems_tagname_a = browser.find_elements_by_xpath("//div[@class='rc']/div[@class='r']/a")
            # idefix = 0
            # for elem in elems_tagname_a:
            #     idefix += 1
            #     url = str(elem.get_attribute("href"))
            #     f = open("/tmp/mitroglou.txt", "w")
            #     f.write(url)
            #     print("b" + str(idefix) + " : " +  url)
            #     f.close()

            liste_titres_h3 = browser.find_elements_by_xpath("//div[@class='rc']/div[@class='r']/a/h3")

            for elt in liste_titres_h3:
                current_url = elt.find_elements_by_xpath("..")[0].get_attribute("href")
                urlList.append(current_url)


                # elems_tagname_a = browser.find_elements_by_tag_name("a")
                # for elem in elems_tagname_a:
                #     url = str(elem.get_attribute("href"))
                #     f = open("/tmp/mitroglou.txt", "w")
                #     f.write(url)
                #     print(url)
                #     f.close()
        browser.quit()
