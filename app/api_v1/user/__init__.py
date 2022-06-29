from fastapi import APIRouter

from . import (
    dependencies,
    responses,
)

router = APIRouter(
    prefix='/registration_requests',
    tags=['Пользователь'],
)

# @router.get('/{user_id}/avatar')
# async def _avatar(user_id: UUID, get_user_photo_case: Depends(get__get_user_photo)):
#     get_user_photo_case.get_photo(user_id)
#     return
