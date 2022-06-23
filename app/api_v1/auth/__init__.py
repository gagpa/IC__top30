from uuid import uuid4

from fastapi import APIRouter, Depends

import domain
from . import (
    client_requests,
    dependencies,
    responses,
)

router = APIRouter(tags=['Авторизация'])


@router.patch(
    '/auth',
    response_model=responses.AccessTokenResponse
)
async def _refresh_token(
        refresh_token: str,
        refresh_token_case: domain.auth.use_cases.refresh_token.RefreshTokenInRepo
        = Depends(dependencies.get__refresh_token_case),
):
    token = await refresh_token_case.refresh(user_id=uuid4(), refresh_token=refresh_token)
    return responses.AccessTokenResponse(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
    )


@router.post(
    '/sign_in',
)
async def _sign_in(
        sign_in: client_requests.SignInRequest,
        auth_case: domain.auth.use_cases.auth.AuthUserInService = Depends(dependencies.get__auth_user_in_service_case),
):
    token = await auth_case.auth(login=sign_in.email, password=sign_in.password)
    return responses.AccessTokenResponse(
        data=responses.Token(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
        )
    )
