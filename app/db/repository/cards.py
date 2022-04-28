from sqlalchemy.orm import Session

from schemas.cards import CardCreate
from db.models.cards import Card
from db.models.users import User


def create_new_card(store_chain_id: int, image_url: str, db: Session, owner: User):
    card_object = Card(owner_username=owner.username, store_chain_id=store_chain_id, image_url=image_url)
    db.add(card_object)
    db.commit()
    db.refresh(card_object)
    return card_object