from typing import Optional

from pydantic import BaseModel


class Response(BaseModel):
    success: bool
    reason: str


class SuccessResponse(Response):
    payload: Optional[dict] = None

    def __init__(self, payload: Optional[dict] = None):
        super().__init__(success=True, reason="")
        self.payload = payload

    def serialize(self) -> dict:
        if self.payload is None:
            return super().model_dump(exclude={'payload'})
        return super().model_dump()


class ErrorResponse(Response):
    def __init__(self, e: Exception):
        super().__init__(success=False, reason=str(e))
