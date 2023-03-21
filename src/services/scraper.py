import io
from multiprocessing.dummy import Pool as ThreadPool

import arxiv
import PyPDF2
import requests

from src.services.conn import get_papers_collection

DOMAINS = [
    "Electronics",
    "Chemistry",
    "Computer",
    "Vision",
    "Logic",
    "Physics",
    "Medicine",
]

db = get_papers_collection()

paper_ids = dict()


def fetch_papers_by_domain(domain):
    total_count = 0
    response = arxiv.Search(query=domain, max_results=500)
    print("Fetching domain success ->", domain, sep=" ")
    papers_text = []
    for paper in response.results():
        try:
            print("Paper -> ", paper.get_short_id())
            # Download the PDF file
            response = requests.get(paper.pdf_url)

            # Open the downloaded content as a PDF object
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content), strict=False)

            # Prevent duplicates
            if paper.entry_id not in paper_ids:
                # Iterate over each page in the PDF file and extract the text
                text = ""
                for page in range(len(pdf_reader.pages)):
                    page_obj = pdf_reader.pages[page]
                    text += page_obj.extract_text()

                papers_text.append(
                    {
                        "id": paper.entry_id,
                        "text": text,
                        "pdf_url": paper.pdf_url,
                        "title": paper.title,
                        "category": paper.primary_category,
                        "authors": [author.name for author in paper.authors],
                        "published": str(paper.published),
                    }
                )

                papers_chunk_len = len(papers_text)
                if papers_chunk_len != 0 and papers_chunk_len % 20 == 0:
                    db.insert_many(papers_text)
                    total_count = papers_chunk_len + total_count
                    print("Pushed", total_count, "in domain ->", domain, sep=" ")

                    papers_text = []

            paper_ids[paper.entry_id] = True
        except Exception as _e:
            print(_e)
            pass

    if len(papers_text) != 0:
        db.insert_many(papers_text)

    print("Completed Fetching papers")


if __name__ == "__main__":
    try:
        pool = ThreadPool(15)
        pool.map(fetch_papers_by_domain, DOMAINS)
    except Exception as _e:
        pass
