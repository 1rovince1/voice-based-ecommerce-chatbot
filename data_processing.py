import os
import pandas as pd
import sqlite3

import fitz
import faiss
from sentence_transformers import SentenceTransformer
import pickle


GENERATED_DIR = "./generated"
ECOMMERCE_DB_PATH = "./generated/database.db"
POLICY_FAISS_INDEX_PATH = "./generated/policy_index.faiss"
POLICY_METADATA_PATH = "./generated/policy_metadata.pkl"
os.makedirs(GENERATED_DIR, exist_ok=True)


# CSV DATA
if not os.path.exists(ECOMMERCE_DB_PATH):
    # data pre-processing
    ECOMMERCE_DATA_FILE_PATH = "./data/ecommerce_data.csv"
    dataframe = pd.read_csv(ECOMMERCE_DATA_FILE_PATH)

    dataframe["InvoiceDate"] = pd.to_datetime(dataframe["InvoiceDate"])

    # DB setup for retrieval
    connection = sqlite3.connect(ECOMMERCE_DB_PATH)
    dataframe.to_sql("ecommerce_table", connection, if_exists="replace")

    connection.close()
else:
    print("ECOMMERCE DB ALREADY EXISTS")


# PDF DATA
if not os.path.exists(POLICY_FAISS_INDEX_PATH):
    POLICY_DATA_FILE_PATH = "./data/ecommerce_policies.pdf"
    policy_doc = fitz.open(POLICY_DATA_FILE_PATH)

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

    faiss.write_index(policy_index, POLICY_METADATA_PATH)
    with open("./policy_metadata.pkl", "wb") as f:
        pickle.dump(content_chunks, f)
else:
    print("FAISS INDEX FOR POLICY ALREADY EXISTS")