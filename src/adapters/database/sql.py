from sqlmodel import create_engine, Session

db_url = f"sqlite:///database.db"
engine = create_engine(db_url, echo=True)


def get_engine():
    return engine


def get_session():
    # https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/#create-a-fastapi-dependency
    with Session(engine) as session:
        yield session
