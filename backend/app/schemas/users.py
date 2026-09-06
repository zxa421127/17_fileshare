from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None
    status: str

    class Config:
        from_attributes = True


class RoleAssign(BaseModel):
    role: str
