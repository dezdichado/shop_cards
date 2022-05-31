from geopy.distance import distance
from sqlalchemy import delete
from sqlalchemy.orm import Session

from schemas.cards import CardCreate
from db.models.cards import Card
from db.models.users import User
from db.models.stores import Store
from db.base import StoreChain


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
        stores = []
        for chain in chains:
            stores.extend(db.query(Store).filter(Store.store_chain_id == chain).all())
        closest = dict()
        addrs = dict()
        for store in stores:
            chain_id = store.store_chain_id
            dist = round(distance((store.latitude, store.longitude),
                         (latitude, longitude)).meters)
            if chain_id in closest:
                if dist < closest[chain_id]:
                    closest[chain_id] = dist
                    addrs[chain_id] = store.address
            else:
                closest[chain_id] = dist
                addrs[chain_id] = store.address
        if len(closest):
            default = max(closest.values()) + 1
        else:
            default = 100
        for chain in chains:
            if chain not in closest:
                closest[chain] = default
                addrs[chain] = None

        for card in cards:
            card.distance = closest[card.store_chain_id]
            card.address = addrs[card.store_chain_id]
        cards.sort(key=lambda x: x.distance)
    return cards


def get_card(id: int, db: Session):
    card = db.query(Card).filter(Card.id == id).first()
    return card


def delete_card(card: Card, db: Session):
    db.execute(delete(Card).where(Card.id == card.id))
    db.commit()


def has_such_card(username: str, store_chain_id: int, db: Session) -> bool:
    cards = db.query(Card).filter(Card.owner_username == username,
                                  Card.store_chain_id == store_chain_id).all()
    return bool(cards)


def is_active_store_chain(id: int, db: Session):
    store_chains = db.query(StoreChain).filter(StoreChain.is_active == True).all()
    return id in {chain.id for chain in store_chains}
