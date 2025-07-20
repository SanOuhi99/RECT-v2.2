from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class MatchStatus(str, Enum):
    """Status of property match"""
    PENDING = "pending"
    REVIEWED = "reviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"

class PropertyType(str, Enum):
    """Types of properties"""
    APARTMENT = "apartment"
    HOUSE = "house"
    VILLA = "villa"
    COMMERCIAL = "commercial"
    LAND = "land"
    OFFICE = "office"
    RETAIL = "retail"

class TransactionType(str, Enum):
    """Types of transactions"""
    SALE = "sale"
    RENT = "rent"
    LEASE = "lease"

class MatchCriteria(BaseModel):
    """Criteria used for property matching"""
    property_type: PropertyType
    transaction_type: TransactionType
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_bedrooms: Optional[int] = None
    max_bedrooms: Optional[int] = None
    min_bathrooms: Optional[int] = None
    max_bathrooms: Optional[int] = None
    min_area: Optional[float] = None  # in square meters
    max_area: Optional[float] = None
    location: Optional[str] = None
    radius: Optional[float] = Field(default=5.0, description="Search radius in kilometers")
    amenities: Optional[List[str]] = []
    additional_filters: Optional[Dict[str, Any]] = {}

class PropertyDetails(BaseModel):
    """Details of a matched property"""
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    property_type: PropertyType
    transaction_type: TransactionType
    price: float
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area: Optional[float] = None
    location: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    amenities: List[str] = []
    images: List[str] = []
    agent_id: uuid.UUID
    agent_name: str
    agent_contact: str
    listing_date: datetime
    updated_at: datetime

class MatchScore(BaseModel):
    """Scoring details for a property match"""
    overall_score: float = Field(..., ge=0, le=100, description="Overall match score (0-100)")
    price_score: float = Field(..., ge=0, le=100)
    location_score: float = Field(..., ge=0, le=100)
    features_score: float = Field(..., ge=0, le=100)
    amenities_score: float = Field(..., ge=0, le=100)
    scoring_factors: Dict[str, float] = {}

# Base schemas
class MatchBase(BaseModel):
    """Base schema for property matches"""
    user_id: uuid.UUID
    criteria: MatchCriteria
    status: MatchStatus = MatchStatus.PENDING
    auto_notify: bool = Field(default=True, description="Auto-notify user of new matches")
    expires_at: Optional[datetime] = None

class MatchCreate(MatchBase):
    """Schema for creating a new match request"""
    pass

    @validator('expires_at')
    def validate_expiry_date(cls, v):
        if v and v <= datetime.utcnow():
            raise ValueError('Expiry date must be in the future')
        return v

class MatchUpdate(BaseModel):
    """Schema for updating match criteria"""
    criteria: Optional[MatchCriteria] = None
    status: Optional[MatchStatus] = None
    auto_notify: Optional[bool] = None
    expires_at: Optional[datetime] = None

    @validator('expires_at')
    def validate_expiry_date(cls, v):
        if v and v <= datetime.utcnow():
            raise ValueError('Expiry date must be in the future')
        return v

class PropertyMatchResult(BaseModel):
    """Individual property match result"""
    id: uuid.UUID
    match_id: uuid.UUID
    property_details: PropertyDetails
    match_score: MatchScore
    matched_at: datetime
    viewed: bool = False
    bookmarked: bool = False
    notes: Optional[str] = None

class MatchResponse(MatchBase):
    """Complete match response with results"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    total_matches: int = 0
    new_matches: int = 0
    last_checked: Optional[datetime] = None
    results: List[PropertyMatchResult] = []

    class Config:
        orm_mode = True

class MatchSummary(BaseModel):
    """Summary of match statistics"""
    id: uuid.UUID
    status: MatchStatus
    total_matches: int
    new_matches: int
    created_at: datetime
    updated_at: datetime
    criteria_summary: str
    expires_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class MatchNotification(BaseModel):
    """Schema for match notifications"""
    match_id: uuid.UUID
    user_id: uuid.UUID
    title: str
    message: str
    notification_type: str = "new_match"
    property_count: int
    sent_at: datetime
    read: bool = False

class MatchAnalytics(BaseModel):
    """Analytics data for matches"""
    total_active_matches: int
    total_properties_matched: int
    average_match_score: float
    top_locations: List[Dict[str, Any]]
    price_range_distribution: Dict[str, int]
    property_type_distribution: Dict[str, int]
    user_engagement_stats: Dict[str, Any]

# Bulk operations
class BulkMatchCreate(BaseModel):
    """Schema for creating multiple matches"""
    matches: List[MatchCreate]
    
    @validator('matches')
    def validate_matches_limit(cls, v):
        if len(v) > 50:  # Limit bulk operations
            raise ValueError('Cannot create more than 50 matches at once')
        return v

class BulkMatchResponse(BaseModel):
    """Response for bulk match creation"""
    created_matches: List[MatchResponse]
    failed_matches: List[Dict[str, Any]]
    total_created: int
    total_failed: int
