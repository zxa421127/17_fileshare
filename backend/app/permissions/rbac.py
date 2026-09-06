from app.database.models import User


def has_permission(
    user:User,
    permission:str
):

    for role in user.roles:

        if permission in [
            "file:read",
            "file:download"
        ]:

            return True


    return False
