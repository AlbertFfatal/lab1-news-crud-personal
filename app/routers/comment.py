from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user, get_comment_for_user
from app.models import User as UserModel, Comment as CommentModel

router = APIRouter(prefix="/comments", tags=["comments"])

# Чтение открыто
@router.get("/", response_model=list[schemas.CommentOut])
def read_comments(db: Session = Depends(get_db)):
    return crud.get_comments(db)

@router.get("/{comment_id}", response_model=schemas.CommentOut)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

# Создание — любой авторизованный
@router.post("/", response_model=schemas.CommentOut)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return crud.create_comment(db, comment)

# Обновление/удаление — owner or admin
@router.put("/{comment_id}", response_model=schemas.CommentOut)
def update_comment(comment_id: int, comment_update: schemas.CommentUpdate, db: Session = Depends(get_db), comment: CommentModel = Depends(get_comment_for_user)):
    return crud.update_comment(db, comment_id, comment_update)

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), comment: CommentModel = Depends(get_comment_for_user)):
    crud.delete_comment(db, comment_id)
    return {"detail": "Comment deleted"}