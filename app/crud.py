from __future__ import annotations

from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas

# User CRUD
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# News CRUD
def get_news(db: Session) -> List[models.News]:
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

def update_news(db: Session, news_id: int, news_update: schemas.NewsUpdate) -> Optional[models.News]:
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
def get_comments(db: Session) -> List[models.Comment]:
    return db.query(models.Comment).all()

def get_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def create_comment(db: Session, comment: schemas.CommentCreate) -> models.Comment:
    db_comment = models.Comment(**comment.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentUpdate) -> Optional[models.Comment]:
    db_comment = get_comment(db, comment_id)
    if not db_comment:
        return None
    update_data = comment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment