from typing import Optional

from fastapi import Depends
from sqlmodel import Session, select
from src.adapters.database.sql import get_session
from src.app.Account import (
    Account,
    AccountRepository,
)


class SqlAccountRepository(AccountRepository):
    def __init__(self, sess: Session = Depends(get_session)) -> None:
        self.session = sess

    def create_account(self, account: Account):
        self.session.add(account)
        self.session.commit()

    def find_account_by_username(self, username: str) -> Optional[Account]:
        statement = select(Account).where(Account.username == username)
        result = self.session.exec(statement)
        account = result.first()
        return account

    def update_account(self, account: Account):
        self.session.add(account)
        self.session.commit()

    def delete_account(self, account: Account):
        self.session.delete(account)
        self.session.commit()
