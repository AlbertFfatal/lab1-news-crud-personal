from fastapi import FastAPI
from .routers import user, news, comment
from .auth.router import router as auth_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
app = FastAPI(
    title="News CRUD API",
    description="CRUD для пользователей, новостей и комментариев",
    version="1.0.0"
)

app.include_router(user.router)
app.include_router(news.router)
app.include_router(comment.router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "News CRUD API is running"}

@app.get("/test")
def test():
    return {"status": "ok", "message": "Server is running without DB"}