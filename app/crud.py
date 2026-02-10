from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas
from app.cache import cache_get, cache_set, cache_delete
from schemas import NewsOut, UserOut


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def get_news(db: Session):
    return db.query(models.News).all()


def get_news_by_id(db: Session, news_id: int) -> Optional[models.News]:
    return db.query(models.News).filter(models.News.id == news_id).first()


def create_news(db: Session, news: schemas.NewsCreate) -> models.News:
    author = get_user(db, news.author_id)
    if not author or not author.is_author_verified:
        raise ValueError("Author is not verified")
    db_news = models.News(**news.model_dump())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def update_news(db: Session, news_id: int, news_update: schemas.NewsUpdate):
    db_news = get_news_by_id(db, news_id)
    if not db_news:
        return None
    update_data = news_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_news, key, value)
    db.commit()
    db.refresh(db_news)
    return db_news


def delete_news(db: Session, news_id: int) -> Optional[models.News]:
    db_news = get_news_by_id(db, news_id)
    if db_news:
        db.delete(db_news)
        db.commit()
    return db_news


# Comment CRUD
def get_comments(db: Session):
    return db.query(models.Comment).all()


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentUpdate):
    db_comment = get_comment(db, comment_id)
    if not db_comment:
        return None
    update_data = comment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# новость по id (Cache-Aside)
def get_news_cached(db: Session, news_id: int):
    key = f"news:{news_id}"
    cached = cache_get(key)
    if cached:
        # Из кэша — JSON - схема - имодель
        news_out = NewsOut.model_validate_json(cached)
        news = models.News(**news_out.model_dump())
        return news
    # Из БД
    news = get_news_by_id(db, news_id)
    if news:
        # в кэш через аут - без полей внутри
        news_out = NewsOut.from_orm(news)
        cache_set(key, news_out.model_dump_json(), ttl=300)
    return news


def invalidate_news_cache(news_id: int):
    key = f"news:{news_id}"
    cache_delete(key)


def get_user_cached(db: Session, user_id: int) -> Optional[models.User]:
    key = f"user:{user_id}"
    cached = cache_get(key)
    if cached:
        user_out = UserOut.model_validate_json(cached)
        user = models.User(**user_out.model_dump())
        user.password_hash = None
        return user
    user = get_user(db, user_id)
    if user:
        user_out = UserOut.from_orm(user)
        cache_set(key, user_out.model_dump_json(), ttl=900)
    return user


def invalidate_user_cache(user_id: int):
    key = f"user:{user_id}"
    cache_delete(key)