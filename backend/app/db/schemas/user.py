from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    company_code: str
    kvcore_token: str

class UserInDB(UserBase):
    id: int
    is_active: bool
    company_id: int

    class Config:
        orm_mode = True