from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.adapters.api.Account import AccountRouter
from src.adapters.api.util import ErrorResponse


def router() -> FastAPI:
    mux = FastAPI()
    mux.add_exception_handler(RequestValidationError, validation_exception_handler)

    mux.include_router(AccountRouter)
    return mux


async def validation_exception_handler(req: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(exc).dict(),
    )
