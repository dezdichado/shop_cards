import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
with open("secrets.json") as f:
    secrets = json.load(f)
cloudinary.config(**(secrets["cloudinary"]))

from fastapi import APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Depends, HTTPException, status, UploadFile

from db.session import get_db
from db.models.users import User
from schemas.cards import CardCreate, ShowCard
from db.repository.cards import create_new_card, list_cards, delete_card,\
     get_card, has_such_card, is_active_store_chain
from apis.version1.route_login import get_current_user_from_token

router = APIRouter()


@router.post("/add", response_model=ShowCard)
def add_card(store_chain_id: int, image: UploadFile, owner: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    if not owner:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized")
    print(owner.username)
    if not is_active_store_chain(store_chain_id, db):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="This store chain ID is not supported")
    if has_such_card(owner.username, store_chain_id, db):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Card for this store chain already exists")
    try:
        response = cloudinary.uploader.upload(image.file, transformation=[{"width": 0.87, "height": 0.7, "crop": "crop"},
                                                                          {"width": 1500, "height": 2000, "crop": "limit"}])
    except cloudinary.exceptions.Error as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=str(err))
    image_url = response["secure_url"]
    card = create_new_card(store_chain_id=store_chain_id, image_url=image_url, db=db, owner=owner)
    return card


@router.get("/", response_model=List[ShowCard])
def get_cards(latitude: Optional[float] = None, longitude: Optional[float] = None, owner: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    if not owner:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized")
    print(owner.username)
    return list_cards(owner, latitude, longitude, db)


@router.delete("/{id}")
def remove_card(id: int, owner: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    card = get_card(id, db)
    # TODO: deleting image from Cloudinary
    if card is None or card.owner_username != owner.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"This user does not have such card")
    delete_card(card, db)
    return {"details": "success"}
