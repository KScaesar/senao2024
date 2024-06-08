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


class PasswordVerificationLimitExceeded(AccountError):
    msg = "Too many password verification attempts. Please wait 1 minute before trying again."

    def __init__(self):
        super().__init__(self.msg)


class UsernameNotFoundError(AccountError):

    def __init__(self, username: str):
        super().__init__(f"username='{username}' not found")
