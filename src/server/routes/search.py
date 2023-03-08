from __future__ import annotations

from fastapi import APIRouter

from services.conn import get_database

router = APIRouter()
db = get_database()


@router.get("/")
def index():
    return {
        "detail": "Welcome to IRSRP",
    }


@router.get("/search", tags=["search_paper"])
def view_a(search_text: str):
    return {"detail": "This is search paper", "params": {"search_text": search_text}}
