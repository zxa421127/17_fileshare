from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.config import settings
from app.database.database import get_db
from app.database.models import FileObject, User
from app.schemas.files import DownloadResponse, FileResponse
from app.storage.minio import ObjectStorage, get_storage


router = APIRouter(prefix="/api/files", tags=["files"])


@router.post("/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    storage: ObjectStorage = Depends(get_storage),
):
    content = await file.read(settings.max_upload_bytes + 1)
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=413,
            detail="File exceeds upload size limit",
        )
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty files are not allowed",
        )

    original_name = file.filename or "unnamed"
    content_type = file.content_type or "application/octet-stream"
    object_name = f"{current_user.id}/{uuid4().hex}"

    try:
        storage.upload_bytes(object_name, content, content_type)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Object storage is unavailable",
        ) from exc

    record = FileObject(
        original_name=original_name,
        object_name=object_name,
        content_type=content_type,
        size=len(content),
        owner_id=current_user.id,
        status="active",
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("", response_model=list[FileResponse])
def list_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(FileObject)
        .filter(
            FileObject.owner_id == current_user.id,
            FileObject.status == "active",
        )
        .order_by(FileObject.created_at.desc(), FileObject.id.desc())
        .all()
    )


@router.get("/{file_id}", response_model=FileResponse)
def get_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(FileObject)
        .filter(
            FileObject.id == file_id,
            FileObject.owner_id == current_user.id,
            FileObject.status == "active",
        )
        .first()
    )
    if record is None:
        raise HTTPException(status_code=404, detail="File not found")
    return record


@router.get("/{file_id}/download", response_model=DownloadResponse)
def get_download_url(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    storage: ObjectStorage = Depends(get_storage),
):
    record = (
        db.query(FileObject)
        .filter(
            FileObject.id == file_id,
            FileObject.owner_id == current_user.id,
            FileObject.status == "active",
        )
        .first()
    )
    if record is None:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        url = storage.presigned_download_url(
            record.object_name,
            settings.download_url_expire_seconds,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Object storage is unavailable",
        ) from exc

    return DownloadResponse(
        file_id=record.id,
        url=url,
        expires_in=settings.download_url_expire_seconds,
    )
