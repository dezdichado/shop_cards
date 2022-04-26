from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from schemas.users import ShowUser
from db.models.users import User
from apis.version1.route_login import get_current_user_from_token

main_methods_router = APIRouter()


@main_methods_router.get("/me", response_model=ShowUser)
async def get_current_user(current_user: User = Depends(get_current_user_from_token)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized")
    return current_user
