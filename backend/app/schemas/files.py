from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    id: int
    original_name: str
    content_type: str
    size: int
    owner_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DownloadResponse(BaseModel):
    file_id: int
    url: str
    expires_in: int
