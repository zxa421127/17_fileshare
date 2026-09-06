from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.database.database import get_db
from app.database.models import (
    FilePermission,
    FileObject,
    User
)

from app.schemas.permissions import PermissionCreate


router = APIRouter(
    prefix="/api/files",
    tags=["permissions"]
)



@router.post("/{file_id}/permissions")
def add_permission(
    file_id:int,
    data:PermissionCreate,
    db:Session=Depends(get_db)
):

    file=db.query(FileObject).filter(
        FileObject.id==file_id
    ).first()


    if not file:
        raise HTTPException(
            404,
            "file not found"
        )


    user=db.query(User).filter(
        User.id==data.user_id
    ).first()


    if not user:
        raise HTTPException(
            404,
            "user not found"
        )


    item=FilePermission(
        file_id=file_id,
        user_id=data.user_id,
        permission=data.permission
    )


    db.add(item)
    db.commit()


    return {
        "message":"permission added"
    }




@router.get("/{file_id}/permissions")
def list_permissions(
    file_id:int,
    db:Session=Depends(get_db)
):

    rows=db.query(
        FilePermission
    ).filter(
        FilePermission.file_id==file_id
    ).all()


    return rows

