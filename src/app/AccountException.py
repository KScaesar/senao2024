class AccountError(Exception):
    pass


class DuplicatedUsernameError(AccountError):
    def __init__(self, msg=None):
        if msg is None:
            msg = "The username already exists"
        super().__init__(msg)


class InvalidValueError(AccountError):
    def __init__(self, msg=None):
        if msg is None:
            msg = "The value is invalid"
        super().__init__(msg)