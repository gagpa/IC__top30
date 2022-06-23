from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import errors
from domain.auth.resources.authentication_service.errors import AuthenticationError
from domain.auth.resources.password_hasher.errors import InvalidPassword


def add_handlers(app: FastAPI):
    app.exception_handler(errors.EntityNotFounded)(_entity_not_founded)
    app.exception_handler(errors.EntityAlreadyExist)(_entity_already_exist)
    app.exception_handler(RequestValidationError)(_request_validation)
    app.exception_handler(HTTPException)(_http_exception)


async def _entity_not_founded(request: Request, exc: errors.EntityNotFounded):
    return JSONResponse(
        status_code=404,
        content={
            'status': False,
            'data': {
                'error': 'entity not founded',
                'detail': 'Сущность не найдена',
            }
        }
    )


async def _entity_already_exist(request: Request, exc: errors.EntityAlreadyExist):
    return JSONResponse(
        status_code=409,
        content={
            'status': False,
            'data': {
                'error': 'entity already exist',
                'detail': 'Сущность уже существует',
            },
        },
    )


async def _request_validation(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            'status': False,
            'data': {
                'error': 'request validation error',
                'detail': 'В запросе найдены не корректные поля',
                'body': exc.body,
            },
        }
    )


async def _http_exception(request: Request, exc: HTTPException):
    headers = getattr(exc, 'headers', None)
    if headers:
        return JSONResponse(
            {'detail': exc.detail}, status_code=exc.status_code, headers=headers
        )
    else:
        return JSONResponse(
            {
                'status': False,
                'data': {
                    'error': 'http error',
                    'detail': exc.detail
                },
            },
            status_code=exc.status_code,
        )


async def _invalid_password(request: Request, exc: InvalidPassword):
    return JSONResponse(
        content={
            'status': False,
            'data': {
                'error': 'auth error',
                'detail': 'Неверные учётные данные'
            },
        },
        status_code=401,
    )


async def _auth_error(request: Request, exc: AuthenticationError):
    return JSONResponse(
        content={
            'status': False,
            'data': {
                'error': 'auth error',
                'detail': 'Неверные учётные данные'
            },
        },
        status_code=401,
    )
