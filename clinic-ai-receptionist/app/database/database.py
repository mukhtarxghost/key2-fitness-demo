import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Use SQLite for demo — no external DB needed
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///key2_fitness.db"
)

if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "mysql://",
        "mysql+pymysql://",
        1,
    )

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
