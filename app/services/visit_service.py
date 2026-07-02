from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.visit import Visit, VisitStatus
from app.models.visitor import Visitor

from app.schemas.visit_schema import (
    VisitCreate,
    VisitUpdate
)

from app.utils.validators import validate_checkout


class VisitService:

    @staticmethod
    def create_visit(
        db: Session,
        visit: VisitCreate
    ):

        # ----------------------------
        # Check Visitor Exists
        # ----------------------------

        visitor = db.query(Visitor).filter(
            Visitor.id == visit.visitor_id
        ).first()

        if visitor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visitor not found."
            )

        # ----------------------------
        # Duplicate Active Visit Check
        # ----------------------------

        active_visit = db.query(Visit).filter(
            and_(
                Visit.visitor_id == visit.visitor_id,
                Visit.status.in_([
                    VisitStatus.SCHEDULED,
                    VisitStatus.CHECKED_IN
                ])
            )
        ).first()

        if active_visit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Visitor already has an active visit."
            )

        # ----------------------------
        # Check-out Validation
        # ----------------------------

        if not validate_checkout(
            visit.check_in,
            visit.check_out
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Check-out time must be greater than check-in."
            )

        db_visit = Visit(
            visitor_id=visit.visitor_id,
            host_name=visit.host_name,
            department=visit.department,
            visit_date=visit.visit_date,
            check_in=visit.check_in,
            check_out=visit.check_out,
            status=visit.status
        )

        db.add(db_visit)
        db.commit()
        db.refresh(db_visit)

        return db_visit

    @staticmethod
    def get_all_visits(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        offset = (page - 1) * limit

        visits = (
            db.query(Visit)
            .offset(offset)
            .limit(limit)
            .all()
        )

        total = db.query(Visit).count()

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": visits
        }

    @staticmethod
    def get_visit_by_id(
        db: Session,
        visit_id: int
    ):

        visit = db.query(Visit).filter(
            Visit.id == visit_id
        ).first()

        if visit is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visit not found."
            )

        return visit
    
    @staticmethod
    def update_visit(
        db: Session,
        visit_id: int,
        visit_data: VisitUpdate
    ):

        visit = db.query(Visit).filter(
            Visit.id == visit_id
        ).first()

        if visit is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visit not found."
            )

        update_data = visit_data.model_dump(exclude_unset=True)

        new_check_in = update_data.get(
            "check_in",
            visit.check_in
        )

        new_check_out = update_data.get(
            "check_out",
            visit.check_out
        )

        new_status = update_data.get(
            "status",
            visit.status
        )

        # ---------------------------------------
        # Check-out must be after Check-in
        # ---------------------------------------

        if not validate_checkout(
            new_check_in,
            new_check_out
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Check-out time must be greater than check-in."
            )

        # ---------------------------------------
        # Cannot Check Out before Check In
        # ---------------------------------------

        if (
            new_status == VisitStatus.CHECKED_OUT
            and new_check_in is None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot check out before check in."
            )

        # ---------------------------------------
        # Cannot mark Checked Out without checkout time
        # ---------------------------------------

        if (
            new_status == VisitStatus.CHECKED_OUT
            and new_check_out is None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Check-out time is required."
            )

        # ---------------------------------------
        # Checked In requires check-in time
        # ---------------------------------------

        if (
            new_status == VisitStatus.CHECKED_IN
            and new_check_in is None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Check-in time is required."
            )

        for key, value in update_data.items():
            setattr(
                visit,
                key,
                value
            )

        db.commit()
        db.refresh(visit)

        return visit

    @staticmethod
    def delete_visit(
        db: Session,
        visit_id: int
    ):

        visit = db.query(Visit).filter(
            Visit.id == visit_id
        ).first()

        if visit is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visit not found."
            )

        db.delete(visit)
        db.commit()

        return {
            "message": "Visit deleted successfully."
        }
    
    @staticmethod
    def filter_visits(
        db: Session,
        visit_date: date = None,
        status: VisitStatus = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Visit)

        if visit_date:
            query = query.filter(
                Visit.visit_date == visit_date
            )

        if status:
            query = query.filter(
                Visit.status == status
            )

        total = query.count()

        visits = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": visits
        }
    
    @staticmethod
    def today_visitors(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        today = date.today()

        query = db.query(Visit).filter(
            Visit.visit_date == today
        )

        total = query.count()

        visits = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": visits
        }