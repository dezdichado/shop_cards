import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
with open("secrets.json") as f:
    secrets = json.load(f)
cloudinary.config(**(secrets["cloudinary"]))

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, UploadFile, File

from db.session import get_db
from db.models.users import User
from schemas.cards import CardCreate, ShowCard
from db.repository.cards import create_new_card
from apis.version1.route_login import get_current_user_from_token

router = APIRouter()


@router.post("/add", response_model=ShowCard)
def add_card(store_chain_id: int, image: UploadFile, owner: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    if not owner:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized")
    try:
        response = cloudinary.uploader.upload(image.file)
    except cloudinary.exceptions.Error as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=str(err))
    image_url = response["secure_url"]
    card = create_new_card(store_chain_id=store_chain_id, image_url=image_url, db=db, owner=owner)
    return card
