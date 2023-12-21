import statisticsLabLocator
from request import Request
from pubmedGetInfo import get_useful_pubmed_info
import pandas as pd
import nlp_similarity
from lablocatortimer import calculate_running_time
from ReportGenerator.pdfGenerator import generate_pdf_report, generate_pdf_report_no_results


# inputs should be defined outside, like a json file
KEYWORDS = ["ghrelin", "fatty acid"]

FIRST_ABSTRACT = """Abstract
The hunger hormone ghrelin (G) is classified as prohibited substance in professional
sport by the World Anti-Doping Agency (WADA), due to its known growth hormone
releasing properties. The endogenous bioactive peptide consists of 28 amino acids
with a caprylic acid attached to serine at position 3. Within this study, it was aimed
to develop methods to determine G and desacyl ghrelin (DAG) in plasma and urine by
means of LC–MS/MS. Two strategies were applied with a bottom-up approach for
plasma and top-down analyses for urine. Both sample preparation procedures were
based on solid-phase extraction for enrichment and sample clean-up. Method validation showed good results for plasma and urine with limits of detection (LODs) for G
and DAG between 30 and 50 pg/ml, recoveries between 45–50%, and imprecisions
(intra- and inter-day) between 3% and 24%. Plasma analysis was also valid for quantification with accuracies determined with 100% for G and 106% for DAG. The
minimum required performance level for doping control laboratories is set to 2 ng/ml
in urine, and the herein established method yielded acceptable results even at 5% of
this level. As proof-of-concept, plasma levels (G and DAG) of healthy volunteers were
determined and ranged between 30 and 100 pg/ml for G and 100–1200 pg/ml for
DAG. In contrast to earlier reported studies using ligand binding assays for urinary G
and DAG, in this mass spectrometry-based study, no endogenous urinary G and DAG
were found, although the LODs should enable this."""


INPUTPARAMS = {
    'abstract' : FIRST_ABSTRACT,
    'region_of_interest' : 'Europe',
    'req_id' : 'test_case_7',
    'request_person' : 'Theo van Kempen',
    'keywords' : KEYWORDS
    }

def main(keywords, inputparams):

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

if __name__ == "__main__":
    result_df = main(KEYWORDS,INPUTPARAMS)