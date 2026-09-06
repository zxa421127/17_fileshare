from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import FilePermission, FileObject, User
from app.api.auth import get_current_user


router = APIRouter(
    prefix="/api/files",
    tags=["permissions"]
)


@router.post("/{file_id}/permissions")
def add_permission(
    file_id:int,
    user_id:int,
    permission:str="read",
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):

    file=db.query(FileObject).filter(
        FileObject.id==file_id,
        FileObject.owner_id==current_user.id
    ).first()

    if not file:
        raise HTTPException(
            status_code=403,
            detail="Only owner can share"
        )


    item=FilePermission(
        file_id=file_id,
        user_id=user_id,
        permission=permission
    )

    db.add(item)
    db.commit()


    return {
        "message":"permission added"
    }


@router.get("/{file_id}/permissions")
def list_permissions(
    file_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):

    return db.query(
        FilePermission
    ).filter(
        FilePermission.file_id==file_id
    ).all()



@router.delete("/{file_id}/permissions/{user_id}")
def delete_permission(
    file_id:int,
    user_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):

    item=db.query(
        FilePermission
    ).filter(
        FilePermission.file_id==file_id,
        FilePermission.user_id==user_id
    ).first()


    if item:
        db.delete(item)
        db.commit()


    return {
        "message":"deleted"
    }
