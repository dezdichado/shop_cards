from geopy.distance import distance
from sqlalchemy import delete
from sqlalchemy.orm import Session

from schemas.cards import CardCreate
from db.models.cards import Card
from db.models.users import User
from db.models.stores import Store


def create_new_card(store_chain_id: int, image_url: str, db: Session, owner: User):
    card_object = Card(owner_username=owner.username, store_chain_id=store_chain_id, image_url=image_url)
    db.add(card_object)
    db.commit()
    db.refresh(card_object)
    return card_object


def list_cards(owner: User, latitude: float, longitude: float, db: Session):
    cards = db.query(Card).filter(Card.owner_username == owner.username).all()
    if latitude and longitude:
        chains = set(card.store_chain_id for card in cards)
        print(chains)
        stores = []
        for chain in chains:
            stores.extend(db.query(Store).filter(Store.store_chain_id == chain).all())
        print([store.store_chain_id for store in stores])
        closest = dict()
        for store in stores:
            chain_id = store.store_chain_id
            dist = round(distance((store.latitude, store.longitude),
                         (latitude, longitude)).meters)
            if chain_id in closest:
                if dist < closest[chain_id]:
                    closest[chain_id] = dist
            else:
                closest[chain_id] = dist
        if len(closest):
            default = max(closest.values()) + 1
        else:
            default = 100
        for chain in chains:
            if chain not in closest:
                closest[chain] = default

        for card in cards:
            card.distance = closest[card.store_chain_id]
        cards.sort(key=lambda x: x.distance)
    return cards


def get_card(id: int, db: Session):
    card = db.query(Card).filter(Card.id == id).first()
    return card


def delete_card(card: Card, db: Session):
    db.execute(delete(Card).where(Card.id == card.id))
    db.commit()
