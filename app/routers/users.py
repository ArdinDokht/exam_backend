from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models import User

router = APIRouter()


@router.get('/me')
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user
