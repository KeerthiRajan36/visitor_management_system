from datetime import date
from datetime import time
from typing import Optional

from pydantic import BaseModel

from app.models.visit import VisitStatus




class VisitCreate(BaseModel):

    visitor_id: int

    host_name: str

    department: str

    visit_date: date

    check_in: Optional[time] = None

    check_out: Optional[time] = None

    status: VisitStatus = VisitStatus.SCHEDULED


class VisitUpdate(BaseModel):

    host_name: Optional[str] = None

    department: Optional[str] = None

    visit_date: Optional[date] = None

    check_in: Optional[time] = None

    check_out: Optional[time] = None

    status: Optional[VisitStatus] = None


class VisitResponse(BaseModel):

    id: int

    visitor_id: int

    host_name: str

    department: str

    visit_date: date

    check_in: Optional[time]

    check_out: Optional[time]

    status: VisitStatus

    class Config:
        from_attributes = True





class VisitFilter(BaseModel):

    visit_date: Optional[date] = None

    status: Optional[VisitStatus] = None

    page: int = 1

    limit: int = 10