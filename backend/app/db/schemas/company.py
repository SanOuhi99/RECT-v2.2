from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str
    code: str

class CompanyCreate(CompanyBase):
    pass

class CompanyInDB(CompanyBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True