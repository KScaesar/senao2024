from pydantic import BaseModel
from typing import Optional


class SuccessResponse(BaseModel):
    success: bool = True
    reason: str = ""
    payload: Optional[dict] = None

    def serialize(self, payload: dict | None = None) -> dict:
        if payload is None:
            return super().model_dump(exclude={'payload'})
        return super().model_dump()

class ErrorResponse(BaseModel):
    success: bool = False
    reason: str

    def __init__(self, e: Exception):
        super().__init__(success=False, reason=str(e))
