from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database import Base


class Visitor(Base):

    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    phone = Column(String(15), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    company = Column(String(150))

    purpose_of_visit = Column(String(255))

    visits = relationship(
        "Visit",
        back_populates="visitor",
        cascade="all, delete"
    )