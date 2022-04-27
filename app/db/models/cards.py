from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Card(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_username = Column(String, ForeignKey("user.username"), nullable=False)
    owner = relationship("User", back_populates="cards")
    store_chain_id = Column(Integer, ForeignKey("storechain.id"), nullable=False)
    store_chain = relationship("StoreChain", back_populates="cards")
    image_url = Column(String, nullable=False)
