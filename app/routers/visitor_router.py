from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.visitor_schema import (
    VisitorCreate,
    VisitorUpdate
)

from app.services.visitor_service import VisitorService

from app.utils.roles import receptionist_or_admin

router = APIRouter(
    prefix="/visitors",
    tags=["Visitors"]
)


@router.post("")
def create_visitor(
    visitor: VisitorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitorService.create_visitor(
        db,
        visitor
    )


@router.get("")
def get_all_visitors(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitorService.get_all_visitors(
        db,
        page,
        limit
    )


@router.get("/{visitor_id}")
def get_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitorService.get_visitor_by_id(
        db,
        visitor_id
    )


@router.put("/{visitor_id}")
def update_visitor(
    visitor_id: int,
    visitor: VisitorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitorService.update_visitor(
        db,
        visitor_id,
        visitor
    )


@router.delete("/{visitor_id}")
def delete_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitorService.delete_visitor(
        db,
        visitor_id
    )


@router.get("/search/")
def search_visitors(
    keyword: str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(receptionist_or_admin)
):
    return VisitorService.search_visitors(
        db,
        keyword,
        page,
        limit
    )