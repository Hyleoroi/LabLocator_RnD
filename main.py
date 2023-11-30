import statisticsLabLocator
from request import Request
from pubmedGetInfo import get_useful_pubmed_info
import pandas as pd
import nlp_similarity
from lablocatortimer import calculate_running_time
from ReportGenerator.pdfGenerator import generate_pdf_report


# inputs should be defined outside, like a json file
KEYWORDS = ["lactulose", "mannitol", "serum", "blood"]

FIRST_ABSTRACT = """To date, tests of small intestinal passive permeability have involved the ingestion of test molecules whose permeation is assessed indirectly by measuring their urinary recovery. Excretion ratios of marker molecules (eg, lactulose-to-mannitol excretion ratio, LMER) are useful clinically. Measurement of permeability markers in serum would improve the convenience of the tests. Our aim was to assess small intestinal permeability in celiac patients using serum lactulose and mannitol levels with calculation of lactulose to mannitol serum ratios (LMSR) and to compare the results with the standard methods using urinary recoveries. Twenty-four newly diagnosed celiacs and 10 control subjects were studied; 10 celiacs were restudied while established on a gluten-free diet. Test subjects and patients ingested 10 g lactulose and 2.5 g mannitol in 50 ml water. In 10 untreated celiacs and the controls, blood was taken from 0 to 120 min and all urine was collected for 6 hr. The remaining 14 untreated and the 10 treated celiacs had a single serum sample taken 60 min after ingestion of the test solution. At 1 hr after ingestion, the mean mannitol level in normals (0.156 mmol/liter) was significantly higher than in untreated celiacs (0.06 mmol/liter). The 1-hr mean serum lactulose level in normals (0.125 micromol/liter) was significantly lower than in untreated celiacs (0.56 micromol/liter). The median 1-hr LMSR in untreated celiacs was 0.42 compared with 0.039 in normals and 0.08 in treated celiacs. There was a significant correlation between LMSR and LMER. Permeability testing using serum measurements of lactulose and mannitol gave comparable results in celiac patients to the tests using urinary recovery of the permeability markers and may prove to be more convenient, especially in pediatric patients."""

INPUTPARAMS = {
    'abstract' : FIRST_ABSTRACT,
    'region_of_interest' : 'Europe',
    'req_id' : '2',
    'request_person' : 'Stefanie Verstringe',
    'keywords' : KEYWORDS
    }

def main(keywords, inputparams):

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

    #Generate a pdf report, everyting is located in .ReportGenerator
    #TODO: @Marcello, this is the final report that needs to be send to the user. The name is a varialbel (request id) Now it is stored in the main folder but this needs to be saved in Sharepoint
    generate_pdf_report(request, result_table, statistics_image)


    #TODO: Is this still needed?
    output = request, result_table, article_count_per_region, similarities, functions_timing # let's discuss the usage of these outputs

    result_df = pd.DataFrame({
        'Pubmed ID' : pmids,
        'Similarity' : similarities,
        'Country' : countries,
        'Abstract' : abstracts,
        'Author name' : authors_names,
        'Affiliation' : affiliations
    })
    return result_df





if __name__ == "__main__":
    result_df = main(KEYWORDS,INPUTPARAMS)