from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from src.model.lda import LDA
from src.services.conn import get_papers_collection
from src.services.fetch_papers import fetch_papers


class Paper(BaseModel):
    id: str
    pdf_url: Optional[str]
    title: str
    category: str
    authors: str
    published: Optional[str]


class SearchQueryResponse(BaseModel):
    results: List[Paper]


router = APIRouter()

papers_collection = get_papers_collection()

lda_model = LDA(docs=fetch_papers(papers_collection))


from pathlib import Path

import os
print(os.getcwd())
model_file = Path("../../lda_model.pkl")
if model_file.is_file():
    # file exists
    print("Model exists, skipping generation")
    lda_model.load_model()
else:
    print("Model does not exist, generating one...")
    lda_model.train_and_save()


@router.get("/")
def index():
    return {
        "detail": "Welcome to IRSRP",
    }


@router.get("/search", tags=["search_paper"])
def query(query: str):
    top_docs = lda_model.predict(query=query)
    results = [
        Paper(
            id=doc["id"],
            pdf_url=doc["pdf_url"],
            title=doc["title"],
            category=doc["category"],
            authors=", ".join(doc["authors"]),
            published=doc["published"],
        )
        for doc in top_docs
    ]
    return SearchQueryResponse(results=results)


print("Hello world")
