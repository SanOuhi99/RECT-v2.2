from sqlalchemy import Column, String, Integer, Float, ForeignKey
from db.models.base import Base

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    price = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    sqft = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="available")
