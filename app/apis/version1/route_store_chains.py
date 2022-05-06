from fastapi import APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Depends, HTTPException, status, UploadFile

from db.session import get_db
from schemas.store_chains import ShowStoreChain
from db.repository.store_chains import list_store_chains

router = APIRouter()


@router.get("/", response_model=List[ShowStoreChain])
def get_store_chains(db: Session = Depends(get_db)):
    return list_store_chains(db)
