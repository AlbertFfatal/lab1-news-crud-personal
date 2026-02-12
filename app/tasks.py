from cache import cache_get, cache_set
from celeryconfig import celery
from app.crud import get_news_by_id, get_users, get_news
from app.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "tasks.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@celery.task(bind=True, default_retry_delay=60, max_retries=5)  # backoff + retries
def send_notification_task(self, news_id: int):
    try:
        db: Session = next(get_db())
        news = get_news_by_id(db, news_id)
        if not news:
            logger.info(f"News {news_id} not found for notification")
            return

        users = get_users(db)
        for user in users:
            if user.email:
                # Идемпотентность: ключ "sent:news:{news_id}:user:{user_id}"
                key = f"sent:news:{news_id}:user:{user.id}"
                if cache_get(key):
                    logger.info(f"Notification already sent to {user.email} for news {news_id} (idempotent)")
                    continue
                logger.info(f"Sent notification to {user.email}: New news '{news.title}' by {news.author.name if news.author else 'Unknown'}")
                cache_set(key, "1", ttl=86400 * 30)  # 30 дней — не отправлять повторно
    except Exception as exc:
        logger.error(f"Notification task failed for news {news_id}: {exc}")
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))  # backoff (60, 120, 180...)

@celery.task(bind=True, default_retry_delay=300, max_retries=3)
def weekly_digest_task(self):
    try:
        db: Session = next(get_db())
        week_ago = datetime.utcnow() - timedelta(days=7)
        all_news = get_news(db)
        news_this_week = [n for n in all_news if n.publication_date and n.publication_date > week_ago]
        users = get_users(db)
        for user in users:
            if user.email:
                logger.info(f"Sent weekly digest to {user.email}: {len(news_this_week)} new(s)")
                for news in news_this_week:
                    author_name = news.author.name if news.author else "Unknown"
                    logger.info(f" - {news.title} by {author_name} ({news.publication_date})")
    except Exception as exc:
        logger.error(f"Weekly digest task failed: {exc}")
        raise self.retry(exc=exc, countdown=300 * (self.request.retries + 1))