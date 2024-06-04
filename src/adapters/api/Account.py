from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

import src.app.AccountException as AccountException
from src.adapters.api.util import (
    SuccessResponse,
    ErrorResponse,
)
from src.app.AccountDto import (
    CreateAccountParams,
    VerifyAccountAndPasswordParams,
)
from src.app.AccountService import AccountService

AccountRouter = APIRouter(
    prefix="/v1/accounts", tags=["account"]
)


@AccountRouter.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponse},
    },
    description="Create a new account",
)
async def create(
      req: CreateAccountParams,
      svc: AccountService = Depends(),
):
    try:
        svc.create_account(req)
        return SuccessResponse().serialize()
    except AccountException.DuplicatedUsernameError as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=ErrorResponse(e).model_dump())
    except AccountException.InvalidValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=ErrorResponse(e).model_dump())
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ErrorResponse(e).model_dump())


@AccountRouter.post(
    "/verify",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponse},
    },
    description=" Verify Username and Password",
)
async def verify(
      req: VerifyAccountAndPasswordParams,
      svc: AccountService = Depends(),
):
    try:
        svc.verify_account_and_password(req)
        return SuccessResponse().serialize()
    except AccountException.DuplicatedUsernameError as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=ErrorResponse(e).model_dump())
    except AccountException.InvalidValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=ErrorResponse(e).model_dump())
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ErrorResponse(e).model_dump())
