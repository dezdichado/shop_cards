from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class ShowUser(BaseModel):
    username: str

    class Config():  # tells pydantic to convert even non dict obj to json
        orm_mode = True


class NewPassword(BaseModel):
    new_password: str
