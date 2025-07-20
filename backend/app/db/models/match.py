# app/db/models/match.py

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    JSON,
    Enum as SqlEnum,
    Float,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.models.base import Base


class MatchStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    VILLA = "villa"
    COMMERCIAL = "commercial"
    LAND = "land"
    OFFICE = "office"
    RETAIL = "retail"


class TransactionType(str, Enum):
    SALE = "sale"
    RENT = "rent"
    LEASE = "lease"


class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Store criteria as JSON for flexibility
    criteria = Column(JSON, nullable=False)

    status = Column(SqlEnum(MatchStatus), nullable=False, default=MatchStatus.PENDING)
    auto_notify = Column(Boolean, default=True)

    expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship example (optional)
    user = relationship("User", back_populates="matches")

    def __repr__(self):
        return f"<Match(id={self.id}, user_id={self.user_id}, status={self.status})>"
