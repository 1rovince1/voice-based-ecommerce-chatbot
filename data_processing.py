import pandas as pd
import sqlite3

import fitz
import faiss
from sentence_transformers import SentenceTransformer
import pickle


# CSV DATA

# data pre-processing
data_file_path = "./data/ecommerce_data.csv"
dataframe = pd.read_csv(data_file_path)

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
        if block[6] == 0: # Only text (each block has 6 elements - 6th is block type, 4th is block text)
            content_chunks.append(block[4])

embedding_model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")
content_embeddings = embedding_model.encode(
    sentences=content_chunks,
    batch_size=32,
    show_progress_bar=True
)

vec_dim = content_embeddings.shape[1]
policy_index = faiss.IndexFlatL2(vec_dim)
policy_index.add(content_embeddings)

faiss.write_index(policy_index, "./policy_index.faiss")
with open("./policy_metadata.pkl", "wb") as f:
    pickle.dump(content_chunks, f)