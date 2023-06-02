import os
import json

class Request:
    def __init__(self, req_id: str, query: str, abstract: str, region_of_interest: str, request_person: str,
                 from_date: int = 1):
        self.req_id = str(req_id)
        self.query = str(query)
        self.abstract = str(abstract)
        self.region_of_interest = str(region_of_interest)
        self.request_person = str(request_person)
        self.from_date = int(from_date)

    def keywords_to_query(*argv: str):
        """
        Specific query request generator for https://pubmed.ncbi.nlm.nih.gov/.
        It combines all keywords into one query string that can be used on pubmed site via RestAPI.
        :param argv: Keyword/sentence
        :return: query usable for pubmed, build from combination of all keywords/sentences.
        """
        query = ''
        for arg in argv:
            if not str(arg) == '':
                if query == '':
                    query = str(arg)
                else:
                    query = query + " AND " + str(arg)
        return query
