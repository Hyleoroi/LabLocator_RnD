from pubmedarticle import PubmedArticle
from typing import List
from collections import Counter



def articlecount_per_region(all_articles_data: List[PubmedArticle]):
    attribute_counts = Counter(x.last_author.region for x in all_articles_data if
                               x.last_author is not None and x.last_author.region is not None)
    return attribute_counts
