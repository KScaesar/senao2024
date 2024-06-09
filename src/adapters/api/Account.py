from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

import src.app.AccountException as AccountException
from src.adapters.api.response import (
    Response,
    SuccessResponse,
    ErrorResponse,
)
from src.app.AccountDto import (
    CreateAccountParams,
    VerifyAccountAndPasswordParams,
)
from src.app.AccountService import AccountService

AccountRouter = APIRouter(
    prefix="/api/v1/accounts", tags=["account"]
)


@AccountRouter.post(
    path="",
    response_model=Response,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
    },
    description="Create a new account",
)
async def create(
      req: CreateAccountParams,
      svc: AccountService = Depends(),
):
    exception_code = {
        AccountException.DuplicatedUsernameError: status.HTTP_409_CONFLICT,
        AccountException.InvalidValueError: status.HTTP_400_BAD_REQUEST,
    }

    try:
        svc.create_account(req)
        return SuccessResponse().serialize()
    except (Exception) as e:
        return JSONResponse(
            status_code=exception_code.get(type(e), status.HTTP_500_INTERNAL_SERVER_ERROR),
            content=ErrorResponse(e).model_dump(),
        )


@AccountRouter.post(
    path="/login",
    response_model=Response,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ErrorResponse},
    },
    description=" Verify Username and Password",
)
async def login(
      req: VerifyAccountAndPasswordParams,
      svc: AccountService = Depends(),
):
    exception_code = {
        AccountException.UsernameNotFoundError: status.HTTP_404_NOT_FOUND,
        AccountException.InvalidValueError: status.HTTP_400_BAD_REQUEST,
        AccountException.PasswordVerificationLimitExceeded: status.HTTP_429_TOO_MANY_REQUESTS,
    }

    try:
        svc.login(req)
        return SuccessResponse().serialize()
    except (AccountException.AccountError, Exception) as e:
        return JSONResponse(
            status_code=exception_code.get(type(e), status.HTTP_500_INTERNAL_SERVER_ERROR),
            content=ErrorResponse(e).model_dump(),
        )
