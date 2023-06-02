from pubmedarticle import PubmedArticle
from request import Request
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from LabLocatorTimer import measure_time

import pandas as pd

@measure_time
def cosine_similarity_algorithme(articles: List[PubmedArticle], user_input: Request, max_items: object = 15) -> object:
    """
    Checks the similarity of all the articles abstracts based on the first article in the list.
    The first article abstract has to be manually added. Afterwords some simple standard NLP algorithms are used.
    :rtype: object
    :param articles: List of PubmedArticles
    :param user_input: Request object
    :param max_items: maxmimum of items to report.
    :return: Sorted list of the 15 most similar article abstracts as the Request abstract
    """


    def similarity_formatter(similarity):
        """"
        Change de similarity value to a string value if needed.
        """
        sim = similarity * 100
        sim = str(sim)[0:4]
        sim = sim + '%'
        return sim

    results = []
    documents = []
    index = []
    return_articles = []

    #Add userinput as !first document!.
    documents.append(user_input.abstract)
    index.append('USER')

    for article in articles:
        documents.append(article.abstract)
        index.append(article.pmid)

    count_vectorizer = CountVectorizer(stop_words='english')
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(documents)

    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix,
                      columns=count_vectorizer.get_feature_names_out(),
                      index=index)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    arr = X.toarray()
    x = cosine_similarity(arr)[0]
    i = 1
    for article in articles:
        y = [article.pmid, x[i]]
        i = i + 1
        results.append(y)

    results.sort(key=lambda z: z[1], reverse=True)
    statistics2 = [item[1] for item in results]

    for result in results[0:max_items]:
        for article in articles:
            if result[0] == article.pmid:
                article.similarity = result[1]
                if article.similarity != 0.0:
                    return_articles.append(article)

    return return_articles,statistics2