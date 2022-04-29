from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session):
    user = User(username=user.username,
                password_hash=Hasher.get_password_hash(user.password)
                )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        raise ValueError("User with such username already exists")
    return user


def update_user_password(user: User, new_password: str, db: Session):
    password_hash = Hasher.get_password_hash(new_password)
    db.execute(update(User).where(User.username == user.username).values(password_hash=password_hash))
    db.commit()
    return user
