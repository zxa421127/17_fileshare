from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.files import router as files_router
from app.api.permissions import router as permissions_router
from app.api.users import router as users_router
from app.api.permissions import router as permissions_router
from app.config import settings


app = FastAPI(
    title=f"{settings.app_name} V{settings.app_version}",
)

app.include_router(auth_router)
app.include_router(files_router)
app.include_router(permissions_router)
app.include_router(users_router)
app.include_router(permissions_router)


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
    }



