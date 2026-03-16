import pandas as pd
import sqlite3

import fitz
import faiss
from sentence_transformers import SentenceTransformer


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

content_chunks = []
for page in policy_doc:
    page_text = page.get_text("blocks")
    for block in page_text:
        if block[6] == 0: # Only text
            content_chunks.append(block[4])

embedding_model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")
content_embeddings = embedding_model.encode(
    sentences=content_chunks,
    batch_size=32,
    show_progress_bar=True
)