from request import Request
from pubmedGetInfo import get_useful_pubmed_info
import pandas as pd
import nlp_similarity
from lablocatortimer import calculate_running_time

# inputs should be defined outside, like a json file
KEYWORDS = ["Virus", "stress", "reduction"]

FIRST_ABSTRACT = """Dynamic mechanical loading increases bone density and strength and promotes osteoblast proliferation, differentiation and matrix production, by acting at the gene expression level. Molecular mechanisms through which mechanical forces are conversed into biochemical signalling in bone are still poorly understood. A growing body of evidence point to extracellular nucleotides (i.e., ATP and UTP) as soluble factors released in response to mechanical stimulation in different cell systems. Runx2, a fundamental transcription factor involved in controlling osteoblasts differentiation, has been recently identified as a target of mechanical signals in osteoblastic cells. We tested the hypothesis that these extracellular nucleotides could be able to activate Runx2 in the human osteoblastic HOBIT cell line. We found that ATP and UTP treatments, as well as hypotonic stress, promote a significant stimulation of Runx2 DNA-binding activity via a mechanism involving PKC and distinct mitogen-activated protein kinase cascades. In fact, by using the specific inhibitors SB203580 (specific for p38 MAPK) and PD98059 (specific for ERK-1/2 MAPK), we found that ERK-1/2, but not p38, play a major role in Runx2 activation. On the contrary, another important transcription factor, i.e., Egr-1, that we previously demonstrated being activated by extracellular released nucleotides in this osteoblastic cell line, demonstrated to be susceptible to both ERK-1/2 and p38 kinases. These data suggest a possible differential involvement of these two transcription factors in response to extracellularly released nucleotides.
    The biological relevance of our data is strengthened by the finding that a target gene of Runx2, i.e., Galectin-3, is up-regulated by ATP stimulation of HOBIT cells with a comparable kinetic of that found for Runx2. Since it is known that osteocytes are the primary mechanosensory cells of the bone, we hypothesize that they may signal mechanical loading to osteoblasts through release of extracellular nucleotides.
    Altogether, these data suggest a molecular mechanism explaining the purinoreceptors-mediated activation of specific gene expression in osteoblasts and could be of help in setting up new pharmacological strategies for the intervention in bone loss pathologies. """

INPUTPARAMS = {
    'abstract' : FIRST_ABSTRACT,
    'region_of_interest' : 'Europe',
    'req_id' : '1',
    'request_person' : 'Robin Vandercruyssen',
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

    output = request, result_table, article_count_per_region, similarities, functions_timing # let's discuss the usage of these outputs

    result_df = pd.DataFrame({
        'Pubmed ID' : pmids,
        'Similarity' : similarities,
        'Country' : countries,
        'Abstract' : abstracts,
        'Author name' : authors_names,
        'Affiliation' : affiliations
    })
    # outputs should be saved somewhere as a csv file
    return result_df

if __name__ == "__main__":
    result_df = main(KEYWORDS,INPUTPARAMS)