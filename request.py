import os
import json

class Request:
    def __init__(self, input_dict, query):
        self.req_id = str(input_dict.get('req_id', ''))
        self.query = str(query)
        self.abstract = str(input_dict.get('abstract', ''))
        self.region_of_interest = str(input_dict.get('region_of_interest', ''))
        self.request_person = str(input_dict.get('request_person', ''))
        self.from_date = int(input_dict.get('from_date', 1))

    # i think this function is easier
    def keywords_to_query(keywords):
        """
        Specific query request generator for https://pubmed.ncbi.nlm.nih.gov/.
        It combines all keywords into one query string that can be used on pubmed site via RestAPI.
        :param args: List of keywords or sentences
        :return: Query usable for pubmed, built from the combination of all keywords/sentences.
        """
        query = ' AND '.join(keywords)
        return query

