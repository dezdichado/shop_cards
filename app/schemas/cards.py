from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional


class CardCreate(BaseModel):
    store_chain_id: int
    image: UploadFile


class ShowCard(BaseModel):
    id: int
    store_chain_id: int
    image_url: str
    distance: Optional[int] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True
