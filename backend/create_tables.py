from sqlalchemy import inspect

from database import engine, get_database_info, init_db


def main():
    init_db()
    print("Connected DB:", get_database_info())
    print("Tables:", inspect(engine).get_table_names())


if __name__ == "__main__":
    main()
