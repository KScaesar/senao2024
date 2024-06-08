from sqlmodel import create_engine, Session

# db_url = f"sqlite:///database.db"

# https://stackoverflow.com/questions/54477829/cryptography-is-required-for-sha256-password-or-caching-sha2-password
# db_url = "mysql+pymysql://root:1234@127.0.0.1:3306/testdata"
db_url = "mysql+pymysql://root:1234@mysql.vHost:3306/testdata"
engine = create_engine(db_url, echo=True)


def get_engine():
    return engine


def get_session():
    # https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/#create-a-fastapi-dependency
    with Session(engine) as session:
        yield session
