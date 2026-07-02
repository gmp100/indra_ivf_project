import os
from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker


def load_env_file():
    env_files = [
        Path(__file__).with_name(".env"),
        Path(__file__).resolve().parent.parent / ".env",
    ]

    for env_file in env_files:
        if not env_file.exists():
            continue

        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def get_database_url():
    load_env_file()

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    database = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER", "mysql+pymysql")

    if user and password and database:
        safe_user = quote_plus(user)
        safe_password = quote_plus(password)
        return f"{driver}://{safe_user}:{safe_password}@{host}:{port}/{database}"

    if os.getenv("USE_SQLITE", "").lower() == "true":
        return "sqlite:///./app.db"

    missing_keys = [
        key
        for key, value in {
            "DB_NAME": database,
            "DB_USER": user,
            "DB_PASSWORD": password,
        }.items()
        if not value
    ]
    raise RuntimeError(
        "MySQL config missing in .env: "
        + ", ".join(missing_keys)
        + ". Add DB_HOST, DB_PORT, DB_NAME, DB_USER, and DB_PASSWORD."
    )


SQLALCHEMY_DATABASE_URL = get_database_url()

connect_args = {}
engine_options = {"pool_pre_ping": True}

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    engine_options = {}
elif SQLALCHEMY_DATABASE_URL.startswith("mysql"):
    connect_args["connect_timeout"] = 10

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    **engine_options,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def ensure_database_exists():
    url = make_url(SQLALCHEMY_DATABASE_URL)
    if not url.drivername.startswith("mysql") or not url.database:
        return

    database_name = url.database.replace("`", "``")
    server_url = url.set(database=None)
    server_engine = create_engine(
        server_url,
        connect_args={"connect_timeout": 10},
        pool_pre_ping=True,
    )

    with server_engine.begin() as connection:
        connection.execute(
            text(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
        )


def init_db():
    # Import models here so Base.metadata knows every table before create_all runs.
    import models  # noqa: F401

    try:
        ensure_database_exists()
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        raise RuntimeError(
            "Database connection failed. Check DB host, port, database name, "
            "internet/firewall access, and credentials."
        ) from exc


def get_database_info():
    url = make_url(SQLALCHEMY_DATABASE_URL)
    return {
        "driver": url.drivername,
        "host": url.host,
        "port": url.port,
        "database": url.database,
    }


# DB Session Dependency injection ke liye
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
