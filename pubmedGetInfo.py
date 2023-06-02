import time
import random
import requests
import re
import logging
import sys
import xml.etree.cElementTree as ET

from request import Request
from author import Author
from pubmedarticle import PubmedArticle
from LabLocatorTimer import measure_time
from statisticsLabLocator import articlecount_per_region

@measure_time
def get_useful_pubmed_info(request: Request):
    """
    Sends a searchquery to pubmedAPI. Only usefull information is extracted and stored. At the end a check is performed
    if the article is inside the region that the user provide.
    :param request: Request object
    :return: List of Article objects that are inside the region of interest that the Request object asked for
    """

    global article_count_per_region
    articlesinfo = []
    articles_in_roi = []

    # TODO: @Marcello Admin value of the app (max items), if not possible to change in the app we change it via Gitpush?
    @measure_time
    def get_all_pubmed_ids(query, max_items=200):
        """
        Generate a GET request for pubmed id's and send to the client
        :param query: basic keyword query
        :param max_items: Maximum articles to be found
        :return: List of all pubmed id's that were found from the provided query
        """

        db = 'pubmed'
        domain = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
        retmode = 'json'
        rettype = 'abstract'

        # max 3 request per second on Pubmed. Include 2-second sleep to prevent blockage of IP address.
        time.sleep(2)

        try:
            get_request_url = f'{domain}/esearch.fcgi?db={db}&retmax={max_items}&retmode={retmode}&rettype={rettype}&term={query}'
            respons = requests.get(get_request_url).json()
            return respons["esearchresult"]["idlist"]
        except requests.exceptions.RequestException as e:
            logging.exception(e, ": Something wrong with the connection from or to pubmed")
            # TODO: @Marcello is it necessary to exit the script if there is an error that interupts the complete flow else return none?
            sys.exit("Exit program: Connection problem with pubmed")
        except KeyError:
            print("Pubmed: no results were found try other query request")
            return None
    def chunk_pubmed_ids_list(pmid_list):
        """
        Al found articles need to be chunked to process. Pubmed is limited to max 100 articles information per request.
        :param pmid_list:List of pubmed ID's
        :return:Chunked list of all the pubmedID's bundled per 100
        """
        chunkedlist = []
        for i in range(0, len(pmid_list), 100):
            chunk = pmid_list[i:i + 100]
            chunk = ','.join(chunk)
            chunkedlist.append(chunk)

        return chunkedlist
    @measure_time
    def get_articles_information(pmid_100_ids_query):
        """
        Generate a GET request for pubmed article data and send to the client
        :param pmid_100_ids_query: max 100 pubmed ID
        :return: XML with 100 articles data.
        """
        db = 'pubmed'
        domain = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
        retmode = 'xml'
        rettype = 'abstract'

        # max 3 request per second on Pubmed. Include random sleep to prevent blockage of IP address.
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)

        try:
            get_request_url = f'{domain}/efetch.fcgi?db={db}&id={pmid_100_ids_query}&retmode={retmode}&rettype={rettype}'
            responsXML = requests.get(get_request_url)
            return responsXML
        except requests.exceptions.RequestException as e:
            logging.exception(e, ": Something wrong with the connection from or to pubmed")
            # TODO: @Marcello is it necessary to exit the script if there is an error that interupts the complete flow else return none?
            sys.exit("Exit program: Connection problem with pubmed")
    @measure_time
    def extract_relevant_information_xml(xmldata):
        """
        Find useful information from the xml delivered from Pubmed and save it for later usage. Check if author has
        affiliation and that there is an abstract linked to the article.
        :param xmldata: array all results from get_articles_information()
        :return: Article object list that is useful
        """

        def get_author_information_from_xml(author_list, id_of_authors):
            """
            Extract author information of the xml article file.
            :param author_list: List of authors per article
            :param id_of_authors: Most of the time only the first and last author is important. So 0 and -1 are commonly used.
            :return: author object
            """
            try:
                lastname = author_list[id_of_authors].find("./LastName").text
                forename = author_list[id_of_authors].find("./ForeName").text
                full_name = lastname + " " + forename
                affiliation = author_list[id_of_authors].find(".//Affiliation").text
                author = Author(full_name, affiliation)
                return author
            except Exception as e:
                return None

        pubmedarticles = []
        for data in xmldata:
            root = ET.fromstring(data.text)
            tree = ET.ElementTree(root)
            for pubmedarticle in tree.findall('./PubmedArticle'):
                try:
                    pmid = pubmedarticle.find("./MedlineCitation/PMID").text
                    url = 'https://pubmed.ncbi.nlm.nih.gov/' + pmid + '/'
                except Exception as e:
                    continue

                try:
                    abstract = pubmedarticle.find(".//AbstractText")
                    a_lst = list(abstract.iter())
                    full_text = ""
                    for y in a_lst:
                        if y.text is not None:
                            full_text = full_text + " " + y.text
                        if y.tail is not None:
                            full_text = full_text + " " + y.tail
                    abstract = full_text
                except:
                    abstract = None
                    continue

                try:
                    authors = pubmedarticle.findall(".//AuthorList/Author")
                except:
                    authors = None
                    continue

                if None not in (authors, abstract):
                    first_author = get_author_information_from_xml(authors, 0)
                    last_author = get_author_information_from_xml(authors, -1)
                    article = PubmedArticle(int(pmid), abstract, first_author, last_author, url)
                    pubmedarticles.append(article)

        return pubmedarticles
    def is_country_in_roi(regionofinterest, author: Author):
        """
        Check if country from the author is in region of input of the user
        :param regionofinterest: Region of interest (location) from the main request.
        :param author: Author object to check
        :return: true if country is in roi (region of interest)
        """
        regionofinterest = re.sub(r"[\[\]]", '', regionofinterest)

        if author is not None:
            if regionofinterest == author.region:
                return True
            return

    pmids = get_all_pubmed_ids(request.query)

    if pmids is not None:
        chunks = chunk_pubmed_ids_list(pmids)
        for x in chunks:
            articlesinfo.append(get_articles_information(x))

        usablearticles = extract_relevant_information_xml(articlesinfo)

        # Swap last and first author  if only first author is in request.region (because the lost author is the most important one, next is the first author)
        articles_in_roi = []
        for y in usablearticles:
            if is_country_in_roi(request.region_of_interest, y.last_author) == True:
                articles_in_roi.append(y)
            elif is_country_in_roi(request.region_of_interest, y.first_author) == True:
                temp = y.last_author
                y.last_author = y.first_author
                y.first_author = temp
                articles_in_roi.append(y)
        article_count_per_region = articlecount_per_region(usablearticles)
    return articles_in_roi, article_count_per_region
