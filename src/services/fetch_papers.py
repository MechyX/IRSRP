def fetch_papers(papers_collection):
    papers = list(papers_collection.find({}))
    return papers