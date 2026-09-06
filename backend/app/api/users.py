from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)


@router.get("")
def list_users():

    return {
        "users":[]
    }


@router.post("")
def create_user(
    username:str
):

    return {
        "username":username,
        "created":True
    }
