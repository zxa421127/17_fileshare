from fastapi import FastAPI
from .api.auth import router as auth_router

app = FastAPI(title="PM Knowledge Portal V1.1")

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "service":"PM Knowledge Portal",
        "version":"1.1"
    }
