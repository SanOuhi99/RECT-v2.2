from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship

from db.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    kvcore_token = Column(String)
    notification_preferences = Column(JSON, default={
        "email": True,
        "frequency": "weekly"
    })
    last_login = Column(DateTime)
    properties = relationship("Property", back_populates="owner")
    clients = relationship("Client", back_populates="agent")
    company = relationship("Company", back_populates="users")
    matches = relationship("Match", back_populates="user")
