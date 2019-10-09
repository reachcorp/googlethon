

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
        if type == "SearchUrl":
            from SearchUrl import SearchUrl
            return SearchUrl()
        assert 0, "Bad shape creation: " + type
    factory = staticmethod(factory)


