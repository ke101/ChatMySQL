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
        return db
    except Exception as e:
        return "Failed", f"Error connecting to the database: {e}"


def execute(query, db):
    # Execute a SQL query and return the result as a DataFrame.
    try:
        df = pd.read_sql(query, db)
        return df
    except:
        return "Error executing query"


def modify(query, db):
    # Execute a SQL query that modifies the database (INSERT, UPDATE, DELETE).
    with db.connect() as conn:
        result = conn.execute(query)
    return f'number of rows affected: {result.rowcount}'
    





def produce_input(db, description=None):
    # Produce the input string for the OpenAI model based on the database schema and sample queries.
    input_str = "Given the following MYSQL tables, your job is to write queries given user’s requests based on the whole conversation."
    if description:
        with open(description, "r") as f:
            data_description = f.read()
            input_str += "\n" + "here are descriptions for each table and sample queries: " + "\n"+ data_description + "\n"
    query = "show tables;"
    tables = execute(query, db)
    for table in tables.values:
        table_name = table[0]
        input_str += f"Table: {table_name}" + "\n"
        query = f"select * from {table_name};"
        df = execute(query, db)
        input_str += str(df.head(1).to_dict(orient="records"))
        input_str += "\n"
    return input_str
