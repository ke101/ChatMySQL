import pymysql as sql
import pandas as pd
import sqlalchemy as engine


def connect_to_db(connection_str):
    """
    Connect to the database using the provided connection string.
    :param connection_str: The connection string for the database.
    :return: A database connection object.
    """
    try:
        db = engine.create_engine(connection_str)
        return db, "Connected to the database successfully."
    except Exception as e:
        return "Failed", f"Error connecting to the database: {e}"


def execute(query, db):
    df = pd.read_sql(query, db)
    return df


# Connect to the database


def produce_input(db):
    input_str = "Given the following MYSQL sample tables, your job is to write queries given user’s requests based on the whole conversation."
    query = "show tables;"
    tables = execute(query, db)
    for table in tables.values:
        table_name = table[0]
        input_str += f"Table: {table_name}" + "\n"
        query = f"select * from {table_name};"
        df = execute(query, db)
        input_str += str(df.head(3).to_dict(orient="records"))
        input_str += "\n"
    return input_str
