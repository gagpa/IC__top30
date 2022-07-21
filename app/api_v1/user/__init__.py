from uuid import UUID

from fastapi import APIRouter, Depends, Response, UploadFile
from fastapi.responses import FileResponse

from domain import user
from . import (
    dependencies,
    responses,
)

router = APIRouter(
    prefix='/user',
    tags=['Пользователь'],
)


@router.get('/{user_id}/avatar')
async def _avatar(
        user_id: UUID,
        find_user_photo_case: user.use_cases.find_photo.FindLastPhoto = Depends(dependencies.get__find_user_photo),
):
    photo = await find_user_photo_case.find(user_id)
    return Response(content=photo, media_type='image/png')


@router.put(
    '/{user_id}/avatar',
    status_code=204,
    response_class=Response,
)
async def _add_avatar(
        _id: UUID,
        photo: UploadFile,
        add_photo_to_user_case: user.use_cases.add_photo.AddPhotoInRepo = Depends(dependencies.get__add_photo_to_user),
):
    await add_photo_to_user_case.add(user_id=_id, photo=photo)


@router.delete(
    '/{_id}/avatar',
    status_code=204,
    response_class=Response,
)
async def _delete_avatar(
        _id: UUID,
        delete_user_photo_case: user.use_cases.delete_user_photo.DeleteUserPhotoFromRepo =
        Depends(dependencies.get__delete_user_photo_from_repo)
):
    await delete_user_photo_case.delete(user_id=_id)
