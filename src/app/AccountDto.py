from pydantic import BaseModel


class CreateAccountParams(BaseModel):
    username: str
    password: str  # plaintext


class VerifyAccountAndPasswordParams(BaseModel):
    username: str
    password: str  # plaintext
