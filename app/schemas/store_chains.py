from pydantic import BaseModel


class ShowStoreChain(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True