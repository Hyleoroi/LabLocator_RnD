import json
import re

class Author:
    def __init__(self, fullname: str, affiliation: str):
        self.fullname = str(fullname)
        self.affiliation = str(affiliation)
        self.country, self.region = self.find_location_author(affiliation)
        self.email = self.find_email_author(affiliation)


    @staticmethod
    def find_location_author(affiliation: str):
        """
        Trying to find geolocation information based on the affiliation of Pubmed. (Affiliation (AD))
        The affiliation data is provided as supplied by the publisher. Publishers are requested to include the following
        data if available, separated by commas: division of the institution, institution name, city, state, postal or
        zip code, country (USA for the United States) followed by a period, then a space followed by the e-mail address.
        :param affiliation: affiliation provided from pubmed as string
        :return: country, region found inside the affiliation text.
        """
        author_country = None
        author_region = None

        try:
            with open('data/GeoInformation.json') as data_file:
                geodata = json.load(data_file)
        except IOError as error:
            print(error)
            print('Geoinformation file is missing from at scout4you-innolab\data\.')

        # pubmed affiliation uses , as delimiter. The country is mostly at the end of the affiliation-field --> reversed
        partition = str(affiliation).rpartition(',')
        for x in reversed(partition):
            for country in geodata:
                if country['Country'].lower() in x.lower():
                    author_country = country['Country']
                    author_region = country['Region']
                    break
                else:
                    author_country = None
                    author_region = None
            if author_country is not None:
                break
        return author_country, author_region

    @staticmethod
    def find_email_author(affiliation: str):
        """
        Trying to find an e-mail address inside the affiliation text from Pubmed. (Affiliation (AD))
        The affiliation data is provided as supplied by the publisher. Publishers are requested to include the following
        data if available, separated by commas: division of the institution, institution name, city, state, postal or
        zip code, country (USA for the United States) followed by a period, then a space followed by the e-mail address.
        :param affiliation: affiliation provided from pubmed as string
        :return: e-mail address when found
        """
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', str(affiliation))
        if match is not None:
            return match.group(0)
        else:
            return None
