import pandas as pd

def identify_process(query):
    """
    Identify the process type of the given SQL query.
    :param query: The SQL query string.
    :return: A string indicating the process type (e.g., "SELECT", "INSERT", "UPDATE", "DELETE").
    """
    query = query.strip().upper()
    if query.startswith("SELECT"):
        return 0
    elif query.startswith("INSERT"):
        return 1
    elif query.startswith("UPDATE"):
        return 1
    elif query.startswith("DELETE"):
        return 1
    else:
        return 0 
    
def identify_output(data):
    if len(data)>=10:
        return 0  # or raise an exception if needed