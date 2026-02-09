from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/", response_model=list[schemas.NewsOut])
def read_news(db: Session = Depends(get_db)):
    return crud.get_news(db)

@router.get("/{news_id}", response_model=schemas.NewsOut)
def read_news(news_id: int, db: Session = Depends(get_db)):
    news = crud.get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.post("/", response_model=schemas.NewsOut)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_news(db, news)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.put("/{news_id}", response_model=schemas.NewsOut)
def update_news(news_id: int, news_update: schemas.NewsUpdate, db: Session = Depends(get_db)):
    news = crud.update_news(db, news_id, news_update)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.delete("/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db)):
    news = crud.delete_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return {"detail": "News and comments deleted"}