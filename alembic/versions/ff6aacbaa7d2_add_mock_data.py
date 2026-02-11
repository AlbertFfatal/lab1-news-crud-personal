"""add mock data

Revision ID: ff6aacbaa7d2
Revises: d350ad05418c
Create Date: 2026-02-09 16:04:12.900486

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ff6aacbaa7d2'
down_revision = 'd350ad05418c'
branch_labels = None
depends_on = None

def upgrade():
    users_table = sa.table('users',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('email', sa.String),
        sa.column('registration_date', sa.DateTime),
        sa.column('is_author_verified', sa.Boolean),
        sa.column('avatar', sa.String)
    )

    news_table = sa.table('news',
        sa.column('id', sa.Integer),
        sa.column('title', sa.String),
        sa.column('content', sa.JSON),
        sa.column('publication_date', sa.DateTime),
        sa.column('author_id', sa.Integer),
        sa.column('cover', sa.String)
    )

    comments_table = sa.table('comments',
        sa.column('id', sa.Integer),
        sa.column('text', sa.String),
        sa.column('news_id', sa.Integer),
        sa.column('author_id', sa.Integer),
        sa.column('publication_date', sa.DateTime)
    )
    op.bulk_insert(users_table, [
        {"name": "Verified Author", "email": "author@example.com", "is_author_verified": True, "avatar": "https://example.com/avatar1.jpg"},
        {"name": "Regular User 1", "email": "user1@example.com", "is_author_verified": False, "avatar": None},
        {"name": "Regular User 2", "email": "user2@example.com", "is_author_verified": False, "avatar": None},
    ])

    op.bulk_insert(news_table, [
        {"title": "News 1", "content": {"text": "Content 1", "blocks": []}, "author_id": 1, "cover": "https://example.com/cover1.jpg"},
        {"title": "News 2", "content": {"text": "Content 2"}, "author_id": 1, "cover": None},
        {"title": "News 3", "content": {"text": "Content 3"}, "author_id": 1, "cover": None},
        {"title": "News 4", "content": {"text": "Content 4"}, "author_id": 1, "cover": None},
        {"title": "News 5", "content": {"text": "Content 5"}, "author_id": 1, "cover": None},
    ])

    op.bulk_insert(comments_table, [
        {"text": "Great news!", "news_id": 1, "author_id": 2},
        {"text": "Thanks for sharing", "news_id": 1, "author_id": 3},
        {"text": "Interesting", "news_id": 2, "author_id": 2},
        {"text": "Good read", "news_id": 3, "author_id": 3},
        {"text": "Agree!", "news_id": 1, "author_id": 2},
        {"text": "Well written", "news_id": 4, "author_id": 3},
        {"text": "Informative", "news_id": 5, "author_id": 2},
        {"text": "Thanks", "news_id": 5, "author_id": 3},
    ])

def downgrade():
    op.execute("TRUNCATE TABLE comments, news, users RESTART IDENTITY CASCADE")