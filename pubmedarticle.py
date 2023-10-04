from author import Author

class PubmedArticle:
    def __init__(self, pmid: int, abstract: str, first_author: Author, last_author: Author, url: str, similarity: float=0):
        self.pmid = int(pmid)
        self.abstract = str(abstract).encode('latin-1', 'replace').decode('latin-1')
        self.first_author: Author = first_author
        self.last_author: Author = last_author
        self.url = str(url)
        self.similarity = float(similarity)
