from fastapi import FastAPI
from app.routers import user, news, comment

app = FastAPI(
    title="News CRUD API",
    description="CRUD для пользователей, новостей и комментариев",
    version="1.0.0"
)

app.include_router(user.router)
app.include_router(news.router)
app.include_router(comment.router)

@app.get("/")
def root():
    return {"message": "News CRUD API is running"}

@app.get("/test")
def test():
    return {"status": "ok", "message": "Server is running without DB"}