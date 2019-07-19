

class SearchFactory:

    def googlesearch_request(self, typ):
        return globals()[typ]()
