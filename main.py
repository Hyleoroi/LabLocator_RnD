import statisticsLabLocator
from request import Request
from pubmedGetInfo import get_useful_pubmed_info
import pandas as pd
import nlp_similarity
from lablocatortimer import calculate_running_time
from ReportGenerator.pdfGenerator import generate_pdf_report, generate_pdf_report_no_results


def main(inputparams):
    querystring = Request.keywords_to_query(inputparams['keywords'])
    request = Request(inputparams, querystring)
    articles_in_roi, article_count_per_region = get_useful_pubmed_info(request)

    if articles_in_roi is not None and articles_in_roi != []:
        result_table, similarities = nlp_similarity.cosine_similarity_algorithme(articles_in_roi, request)
        functions_timing = calculate_running_time()
        statistics_image = statisticsLabLocator.heatmap_generator(request, article_count_per_region)

        #Generate a pdf report, everyting is located in .ReportGenerator
        generate_pdf_report(request, result_table, statistics_image,similarities)
    else:
        generate_pdf_report_no_results(request)