from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class User(Base):
    username = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
