import re

from src.app.AccountException import InvalidValueError

class Account:
    pass


class Validator:
    @staticmethod
    def validate(username: str, password: str):
        Validator.validate_username(username)
        Validator.validate_password(password)

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
