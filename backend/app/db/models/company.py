from sqlalchemy import Column, String, Boolean, Integer, JSON
from sqlalchemy.orm import relationship

from db.models.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    settings = Column(JSON, default={
        "max_users": 10,
        "allowed_counties": []
    })

    users = relationship("User", back_populates="company")
