import pandas as pd
import sqlite3

import fitz


# CSV DATA

# data pre-processing
dataframe = pd.read_csv("./data/ecommerce_data.csv")
dataframe["InvoiceDate"] = pd.to_datetime(dataframe["InvoiceDate"])

# DB setup for retrieval
connection = sqlite3.connect("database.db")
dataframe.to_sql("ecommerce_table", connection, if_exists="replace")

connection.close()


# PDF DATA

policy_file_path = "./data/ecommerce_policies.pdf"
policy_doc = fitz.open(policy_file_path)

for i, page in enumerate(policy_doc):
    text = page.get_text()
    # print(f"Page {i}:\n\n{text}\n\n")