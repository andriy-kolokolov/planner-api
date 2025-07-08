from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_utils.cbv import cbv

from app.schemas.user import UserRead
from app.services.user_service import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@cbv(router)
class Users:
    user_service: UserService = Depends(get_user_service)

    @router.get("/", response_model=list[UserRead], status_code=status.HTTP_200_OK)
    def list(self):
        return self.user_service.list_users()

    @router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
    def read(self, user_id: int):
        db_user = self.user_service.get_user_by_identifier(user_id)
        if not db_user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id {user_id} not found")
        return db_user
