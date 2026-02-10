from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.github import GithubSSO
from app import crud, schemas, models
from app.database import get_db
from app.utils.auth import hash_password, verify_password, create_access_token, create_refresh_token
from app.config import settings
from app.dependencies import get_current_user
from app.cache import save_refresh_session, get_refresh_session, delete_refresh_session, get_user_sessions
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


router = APIRouter(prefix="/auth", tags=["auth"])

github_sso = GithubSSO(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    redirect_uri="http://localhost:8000/auth/github/callback",
    allow_insecure_http=True  #
)

# Local register
@router.post("/register")
def register(user_create: schemas.UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user_create.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user_create.password)
    new_user = models.User(
        name=user_create.name,
        email=user_create.email,
        password_hash=hashed,
        is_author_verified=user_create.is_author_verified,
        is_admin=user_create.is_admin,
        avatar=user_create.avatar
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"detail": "User registered"}

# Local login
@router.post("/login")
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db), request: Request = None):
    user = crud.get_user_by_email(db, user_login.email)
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    user_agent = request.headers.get("user-agent", "unknown") if request else "unknown"

    save_refresh_session(
        refresh_token=refresh_token,
        user_id=user.id,
        user_agent=user_agent,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
# GitHub OAuth
@router.get("/github/login")
async def github_login():
    return await github_sso.get_login_redirect()

@router.get("/github/callback")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    user = await github_sso.verify_and_process(request)
    if not user:
        raise HTTPException(status_code=401, detail="GitHub auth failed")
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        db_user = models.User(
            name=user.display_name or user.email,
            email=user.email,
            is_author_verified=False,
            is_admin=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    access_token = create_access_token({"sub": str(db_user.id)})
    refresh_token = create_refresh_token({"sub": str(db_user.id)})
    user_agent = request.headers.get("user-agent", "unknown")
    save_refresh_session(
        refresh_token=refresh_token,
        user_id= db_user.id,
        user_agent=user_agent,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Refresh
@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    session_data = get_refresh_session(refresh_token)
    if not session_data or datetime.fromisoformat(session_data["expires_at"]) < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    access_token = create_access_token({"sub": str(session_data["user_id"])})
    return {"access_token": access_token, "token_type": "bearer"}

# Logout
@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    delete_refresh_session(refresh_token)
    return {"detail": "Logged out"}

# Сессии пользователя
@router.get("/sessions")
def my_sessions(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_sessions(current_user.id)