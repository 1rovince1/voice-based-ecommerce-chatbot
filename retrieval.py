import pandas as pd
import sqlite3

# DB setup for retrieval
connection = sqlite3.connect("database.db")

def sql_tool(query: str):
    """Run a SQL SELECT query on a SQLite database and return the results."""
    return pd.read_sql_query(query, connection).to_dict(orient="records")