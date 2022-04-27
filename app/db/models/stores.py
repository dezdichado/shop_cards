from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Store(Base):
    id = Column(Integer, primary_key=True, index=True)
    store_chain_id = Column(Integer, ForeignKey("storechain.id"))
    store_chain = relationship("StoreChain", back_populates="stores")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)