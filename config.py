import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

class Config:
    DB_USER = "postgres"
    DB_PASSWORD = "yanam0856"
    DB_NAME = "tasks_habits"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret")  # защита форм

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)

SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

class Base(DeclarativeBase):
    pass

def get_session():
    with SessionLocal() as session:
        yield session
