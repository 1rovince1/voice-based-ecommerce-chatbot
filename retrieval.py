import pandas as pd
import sqlite3

# SQL tool for csv DB query
def sql_tool(query: str):
    """Run a SQL SELECT query on a SQLite database and return the results."""
    try:
        connection = sqlite3.connect("database.db")
        result = pd.read_sql_query(query, connection).to_dict(orient="records")
        connection.close()
        return result
    except Exception as e:
        print(f"Error in running query: {str(e)}")
        return e