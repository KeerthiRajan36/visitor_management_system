from datetime import date

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.visit import VisitStatus

from app.schemas.visit_schema import (
    VisitCreate,
    VisitUpdate
)

from app.services.visit_service import VisitService

from app.utils.roles import receptionist_or_admin

router = APIRouter(
    prefix="/visits",
    tags=["Visits"]
)


@router.post("")
def create_visit(
    visit: VisitCreate,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitService.create_visit(
        db,
        visit
    )


@router.get("")
def get_all_visits(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitService.get_all_visits(
        db,
        page,
        limit
    )


@router.get("/{visit_id}")
def get_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitService.get_visit_by_id(
        db,
        visit_id
    )


@router.put("/{visit_id}")
def update_visit(
    visit_id: int,
    visit: VisitUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitService.update_visit(
        db,
        visit_id,
        visit
    )


@router.delete("/{visit_id}")
def delete_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitService.delete_visit(
        db,
        visit_id
    )


@router.get("/filter/")
def filter_visits(
    visit_date: date = None,
    status: VisitStatus = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitService.filter_visits(
        db,
        visit_date,
        status,
        page,
        limit
    )


@router.get("/today/")
def today_visitors(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitService.today_visitors(
        db,
        page,
        limit
    )