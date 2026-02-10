from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user, get_news_for_user
from app.models import User as UserModel, News as NewsModel
from app.crud import invalidate_news_cache

router = APIRouter(prefix="/news", tags=["news"])

# Чтение открыто
@router.get("/", response_model=list[schemas.NewsOut])
def read_news(db: Session = Depends(get_db)):
    return crud.get_news(db)

@router.get("/{news_id}", response_model=schemas.NewsOut)
def read_news(news_id: int, db: Session = Depends(get_db)):
    news = crud.get_news_cached(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

# Создание — verified or admin
@router.post("/", response_model=schemas.NewsOut)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_author_verified and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Author is not verified")
    news.author_id = current_user.id
    created_news = crud.create_news(db, news)
    invalidate_news_cache(created_news.id)
    return created_news

@router.put("/{news_id}", response_model=schemas.NewsOut)
def update_news(news_id: int, news_update: schemas.NewsUpdate, db: Session = Depends(get_db), news: NewsModel = Depends(get_news_for_user)):
    updated = crud.update_news(db, news_id, news_update)
    invalidate_news_cache(news_id)
    return updated
@router.delete("/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db), news: NewsModel = Depends(get_news_for_user)):
    crud.delete_news(db, news_id)
    invalidate_news_cache(news_id)
    return {"detail": "News and comments deleted"}