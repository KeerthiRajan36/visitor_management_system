from sqlalchemy.orm import Session
from sqlalchemy import or_

from fastapi import HTTPException
from fastapi import status

from app.models.visitor import Visitor
from app.schemas.visitor_schema import (
    VisitorCreate,
    VisitorUpdate
)

from app.utils.validators import validate_phone


class VisitorService:

    @staticmethod
    def create_visitor(
        db: Session,
        visitor: VisitorCreate
    ):

        email_exists = db.query(Visitor).filter(
            Visitor.email == visitor.email
        ).first()

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Visitor email already exists."
            )

        if not validate_phone(visitor.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number."
            )

        db_visitor = Visitor(
            name=visitor.name,
            phone=visitor.phone,
            email=visitor.email,
            company=visitor.company,
            purpose_of_visit=visitor.purpose_of_visit
        )

        db.add(db_visitor)
        db.commit()
        db.refresh(db_visitor)

        return db_visitor

    @staticmethod
    def get_all_visitors(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        offset = (page - 1) * limit

        visitors = (
            db.query(Visitor)
            .offset(offset)
            .limit(limit)
            .all()
        )

        total = db.query(Visitor).count()

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": visitors
        }

    @staticmethod
    def get_visitor_by_id(
        db: Session,
        visitor_id: int
    ):

        visitor = db.query(Visitor).filter(
            Visitor.id == visitor_id
        ).first()

        if visitor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visitor not found."
            )

        return visitor

    @staticmethod
    def update_visitor(
        db: Session,
        visitor_id: int,
        visitor_data: VisitorUpdate
    ):

        visitor = db.query(Visitor).filter(
            Visitor.id == visitor_id
        ).first()

        if visitor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visitor not found."
            )

        if visitor_data.email:

            email_exists = db.query(Visitor).filter(
                Visitor.email == visitor_data.email,
                Visitor.id != visitor_id
            ).first()

            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists."
                )

        if visitor_data.phone:

            if not validate_phone(visitor_data.phone):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid phone number."
                )

        update_data = visitor_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(visitor, key, value)

        db.commit()
        db.refresh(visitor)

        return visitor

    @staticmethod
    def delete_visitor(
        db: Session,
        visitor_id: int
    ):

        visitor = db.query(Visitor).filter(
            Visitor.id == visitor_id
        ).first()

        if visitor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visitor not found."
            )

        db.delete(visitor)
        db.commit()

        return {
            "message": "Visitor deleted successfully."
        }

    @staticmethod
    def search_visitors(
        db: Session,
        keyword: str,
        page: int = 1,
        limit: int = 10
    ):

        offset = (page - 1) * limit

        query = db.query(Visitor).filter(
            or_(
                Visitor.name.ilike(f"%{keyword}%"),
                Visitor.phone.ilike(f"%{keyword}%")
            )
        )

        total = query.count()

        visitors = (
            query.offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": visitors
        }