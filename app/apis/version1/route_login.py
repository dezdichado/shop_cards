from fastapi import APIRouter, Body
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from fastapi import status, HTTPException
from jose import JWTError, jwt

from schemas.users import UserCreate, ShowUser, NewPassword
from db.models.users import User
from db.session import get_db
from db.repository.users import create_new_user, update_user_password
from core.hashing import Hasher
from schemas.tokens import Token
from db.repository.login import get_user
from core.security import create_access_token
from core.config import settings


router = APIRouter()


@router.post("/register", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_new_user(user=user, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return user


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username=username, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password_hash):
        return False
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


@router.put("/change_password", response_model=ShowUser)
def change_password(new_password: NewPassword, user: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    user = update_user_password(user, new_password.new_password, db)
    return user
