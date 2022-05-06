from sqlalchemy.orm import Session

from db.models.store_chains import StoreChain


def list_store_chains(db: Session):
    return db.query(StoreChain).filter(StoreChain.is_active == True).all()
