from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from db.base_class import Base


class StoreChain(Base):
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean)
    stores = relationship("Store", back_populates="store_chain")
    cards = relationship("Card", back_populates="store_chain")