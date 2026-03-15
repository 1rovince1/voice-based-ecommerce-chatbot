import pandas as pd
import sqlite3

# data pre-processing
dataframe = pd.read_csv("./data/ecommerce_data.csv")
dataframe["InvoiceDate"] = pd.to_datetime(dataframe["InvoiceDate"])

# DB setup for retrieval
connection = sqlite3.connect("database.db")
dataframe.to_sql("ecommerce_table", connection, if_exists="replace")

connection.close()