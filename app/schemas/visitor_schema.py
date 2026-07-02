from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class VisitorCreate(BaseModel):

    name: str = Field(min_length=2, max_length=100)

    phone: str = Field(
        pattern=r"^[6-9]\d{9}$"
    )

    email: EmailStr

    company: Optional[str] = None

    purpose_of_visit: Optional[str] = None


class VisitorUpdate(BaseModel):

    name: Optional[str] = None

    phone: Optional[str] = Field(
        default=None,
        pattern=r"^[6-9]\d{9}$"
    )

    email: Optional[EmailStr] = None

    company: Optional[str] = None

    purpose_of_visit: Optional[str] = None


class VisitorResponse(BaseModel):

    id: int

    name: str

    phone: str

    email: EmailStr

    company: Optional[str]

    purpose_of_visit: Optional[str]

    class Config:
        from_attributes = True

    



class VisitorSearch(BaseModel):

    name: Optional[str] = None

    phone: Optional[str] = None

    page: int = 1

    limit: int = 10