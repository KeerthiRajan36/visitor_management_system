from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Time
from sqlalchemy import ForeignKey
from sqlalchemy import Enum

from sqlalchemy.orm import relationship

from app.database import Base

import enum


class VisitStatus(str, enum.Enum):

    SCHEDULED = "Scheduled"

    CHECKED_IN = "Checked In"

    CHECKED_OUT = "Checked Out"

    CANCELLED = "Cancelled"


class Visit(Base):

    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)

    visitor_id = Column(
        Integer,
        ForeignKey("visitors.id"),
        nullable=False
    )

    host_name = Column(
        String(100),
        nullable=False
    )

    department = Column(
        String(100),
        nullable=False
    )

    visit_date = Column(
        Date,
        nullable=False
    )

    check_in = Column(Time)

    check_out = Column(Time)

    status = Column(
        Enum(VisitStatus),
        default=VisitStatus.SCHEDULED,
        nullable=False
    )

    visitor = relationship(
        "Visitor",
        back_populates="visits"
    )