from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    is_author_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)  # Новый флаг админа
    avatar = Column(String)  # URL
    password_hash = Column(String)  # Хэш пароля для local auth (nullable для GitHub users)

    news = relationship("News", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(JSON, nullable=False)
    publication_date = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cover = Column(String)

    author = relationship("User", back_populates="news")
    comments = relationship("Comment", back_populates="news", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    news_id = Column(Integer, ForeignKey("news.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    publication_date = Column(DateTime(timezone=True), server_default=func.now())

    news = relationship("News", back_populates="comments")
    author = relationship("User", back_populates="comments")

# Новая таблица для refresh токенов
class RefreshSession(Base):
    __tablename__ = "refresh_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    refresh_token = Column(Text, unique=True, nullable=False, index=True)
    user_agent = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User")