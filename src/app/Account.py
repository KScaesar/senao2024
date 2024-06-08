import hashlib
import re
import secrets
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

from sqlmodel import SQLModel, Field
from src.adapters.database.sql import get_engine
from src.app.AccountException import (
    InvalidValueError,
    PasswordVerificationLimitExceeded,
)
from ulid import ULID  # https://github.com/mdomke/python-ulid


class Account(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ULID()), max_length=26, primary_key=True)
    username: str = Field(max_length=32, unique=True)
    hashed_password: bytes
    salt: bytes
    created_at: datetime = Field(default_factory=datetime.now)
    verified_at: datetime = Field(default_factory=datetime.now)
    verified_retry_count: int = 5

    @classmethod
    def register(cls, username: str, plaintext_password: str) -> 'Account':
        Validator.validate(username, plaintext_password)

        salt = secrets.token_bytes(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', plaintext_password.encode(), salt, 100000)

        return cls(
            username=username,
            hashed_password=hashed_password,
            salt=salt,
        )

    def login(self, plaintext_password: str) -> bool:
        one_minute = timedelta(minutes=1)

        now = datetime.now()
        verified_interval = now - self.verified_at

        if self.verified_retry_count == 0 and verified_interval < one_minute:
            raise PasswordVerificationLimitExceeded

        if verified_interval >= one_minute:
            self.verified_retry_count = 5

        self.verified_at = now

        hashed_password = hashlib.pbkdf2_hmac('sha256', plaintext_password.encode(), self.salt, 100000)
        if hashed_password == self.hashed_password:
            self.verified_retry_count = 5
            return True

        self.verified_retry_count -= 1
        return False


SQLModel.metadata.create_all(get_engine())


class Validator:
    @classmethod
    def validate(cls, username: str, password: str):
        cls.validate_username(username)
        cls.validate_password(password)

    @staticmethod
    def validate_username(username: str):
        if not re.match(r'^[a-zA-Z0-9_-]{3,32}$', username):
            raise InvalidValueError("username should be with len=[3,32]")

    @staticmethod
    def validate_password(password: str):
        if not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
            raise InvalidValueError("password should be with len=[8,32]")

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password):
            raise InvalidValueError("password should be containing at least 1 uppercase letter, 1 lowercase letter, and 1 number")


class AccountRepository(ABC):
    # https://stackoverflow.com/questions/74910338/its-possible-to-do-dependency-injection-in-fastapi-using-abstract-class

    @abstractmethod
    def create_account(self, account: Account):
        pass

    @abstractmethod
    def find_account_by_username(self, username: str) -> Optional[Account]:
        pass

    @abstractmethod
    def update_account(self, account: Account):
        pass

    @abstractmethod
    def delete_account(self, account: Account):
        pass
