import os

from sqlalchemy import create_engine

def get_db_conn():
    db_host = os.environ["DB_HOST"]
    db_name = os.environ["DB_NAME"]
    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]

    return create_engine(f"mysql+mysqldb://{db_user}:{db_password}@{db_host}/{db_name}")
