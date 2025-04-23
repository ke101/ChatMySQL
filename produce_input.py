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
    if len(df) >= 20:
        idea = input("if output to csv (y/n):")
        if idea == "y":
            file_name = input("Please enter the file name (without extension): ")
            df.to_csv(f"{file_name}.csv", index=False)
            return f"Data exported to {file_name}.csv"
        return df.head(10)
        
    return df


def modify(query, db):
    with db.connect() as conn:
        result = conn.execute(query)
    return f'number of rows affected: {result.rowcount}'
    


# Connect to the database


def produce_input(db, description=None):
    input_str = "Given the following MYSQL tables, your job is to write queries given user’s requests based on the whole conversation."
    if description:
        with open(description, "r") as f:
            data_description = f.read()
            input_str += "\n" + "here's descriptions for each table: " + "\n"+ data_description + "\n"
    query = "show tables;"
    tables = execute(query, db)
    for table in tables.values:
        table_name = table[0]
        input_str += f"Table: {table_name}" + "\n"
        query = f"select * from {table_name};"
        df = execute(query, db)
        input_str += str(df.head(1).to_dict(orient="records"))
        input_str += "\n"
    #print(input_str)
    return input_str
