from pydantic import BaseModel
from fastapi import UploadFile


class CardCreate(BaseModel):
    store_chain_id: int
    image: UploadFile


class ShowCard(BaseModel):
    id: int
    store_chain_id: int
    image_url: str

    class Config:
        orm_mode = True
