import statisticsLabLocator
from request import Request
from pubmedGetInfo import get_useful_pubmed_info
import pandas as pd
import nlp_similarity
from lablocatortimer import calculate_running_time
from ReportGenerator.pdfGenerator import generate_pdf_report

def main(inputparams):

    querystring = Request.keywords_to_query(inputparams['keywords'])
    request = Request(inputparams, querystring)
    articles_in_roi, article_count_per_region = get_useful_pubmed_info(request)
    result_table, similarities = nlp_similarity.cosine_similarity_algorithme(articles_in_roi, request)
    functions_timing = calculate_running_time()
    pmids = [article.pmid for article in articles_in_roi]
    countries = [article.last_author.country for article in articles_in_roi]
    abstracts = [article.abstract for article in articles_in_roi]
    authors_names = [article.last_author.fullname for article in articles_in_roi]
    affiliations = [article.last_author.affiliation for article in articles_in_roi]
    statistics_image = statisticsLabLocator.generate_collection_statics_image(article_count_per_region, similarities, functions_timing)

    generate_pdf_report(request, result_table, statistics_image)