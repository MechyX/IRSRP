import io

import arxiv
import PyPDF2
import requests
from conn import get_database

DOMAINS = ["Electronics", "Chemistry", "Computer", "Vision"]


db = get_database()


for domain in DOMAINS:
    response = arxiv.Search(query=domain, max_results=1)
    papers_text = []
    for paper in response.results():
        # Download the PDF file
        response = requests.get(paper.pdf_url)
        file_size = int(response.headers.get("Content-Length", 0)) / (1024 * 1024)
        print("File size " + str(file_size))

        # Open the downloaded content as a PDF object
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))

        # Iterate over each page in the PDF file and extract the text
        text = ""
        for page in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page]
            text += page_obj.extract_text()

        papers_text.append({"id": paper.entry_id, "text": text})

    db.insert_many(papers_text)
