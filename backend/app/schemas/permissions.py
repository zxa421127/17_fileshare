from pydantic import BaseModel


class PermissionCreate(BaseModel):

    user_id:int

    permission:str="read"
