from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.utils.jwt import get_current_user
from app.models.user import UserRole


def admin_only(
        current_user=Depends(get_current_user)
):

    if current_user.role != UserRole.ADMIN:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


def receptionist_or_admin(
        current_user=Depends(get_current_user)
):

    if current_user.role not in [
        UserRole.ADMIN,
        UserRole.RECEPTIONIST
    ]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    return current_user