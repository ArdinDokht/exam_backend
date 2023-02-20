from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.config.base import settings
from app.dependencies import get_db, get_current_user
from app.models import User
from app.core import security
from app.core.security import verify_password

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
def login_access_token(*, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), response: Response):
    user: User = db.scalars(select(User).filter_by(username=form_data.username)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(user.username)

    # Add secure and domain
    response.set_cookie(key="auth_access_token", value=f"Bearer {access_token}", expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, httponly=True,
                        secure=True, samesite='none', domain=settings.COOKIE_DOMAIN)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }


@router.get("/logout")
async def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie("auth_access_token", secure=True, samesite='none', domain=settings.COOKIE_DOMAIN)
    return {"status": "success"}
