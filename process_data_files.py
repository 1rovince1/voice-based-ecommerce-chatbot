from utils.logger_config import setup_logging
setup_logging()
import logging
import os
import pandas as pd
import sqlite3

import fitz
import faiss
from sentence_transformers import SentenceTransformer
import pickle

from config import settings
logger = logging.getLogger(__name__)

os.makedirs(settings.GENERATED_DIR, exist_ok=True)

# CSV DATA
if not os.path.exists(settings.ECOMMERCE_DB_PATH):
    logger.info("CREATING ECOMMERCE DB...")
    # data pre-processing
    dataframe = pd.read_csv(settings.ECOMMERCE_DATA_FILE_PATH)

    dataframe["InvoiceDate"] = pd.to_datetime(dataframe["InvoiceDate"])

    # DB setup for retrieval
    connection = sqlite3.connect(settings.ECOMMERCE_DB_PATH)
    dataframe.to_sql("ecommerce_table", connection, if_exists="replace")

    connection.close()
    logger.info("ECOMMERCE DB CREATED")
else:
    logger.info("ECOMMERCE DB ALREADY EXISTS")


# PDF DATA
def is_index_valid():
    if not os.path.exists(settings.POLICY_FAISS_INDEX_PATH):
        return False
    if not os.path.exists(settings.POLICY_METADATA_PATH):
        return False
    
    with open(settings.POLICY_METADATA_PATH, "rb") as f:
        policy_metadata = pickle.load(f)
    return (
        policy_metadata.get("embedding_model_name") == settings.EMBEDDING_MODEL_NAME
    )

if not is_index_valid():
    logger.info("CREATING POLICY INDEX...")
    policy_doc = fitz.open(settings.POLICY_DATA_FILE_PATH)

    content_chunks = []
    for page in policy_doc:
        page_text = page.get_text("blocks")
        for block in page_text:
            if block[6] == 0:   # Only text (each block has 6 elements - 6th is block type, 4th is block text)
                content_chunks.append(block[4])

    embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
    content_embeddings = embedding_model.encode(
        sentences=content_chunks,
        batch_size=32,
        show_progress_bar=True
    )

    vec_dim = content_embeddings.shape[1]
    policy_index = faiss.IndexFlatL2(vec_dim)
    policy_index.add(content_embeddings)

    faiss.write_index(policy_index, settings.POLICY_FAISS_INDEX_PATH)
    policy_metadata = {
        "embedding_model_name": settings.EMBEDDING_MODEL_NAME,
        "vector_dimensions": vec_dim,
        "content_chunks": content_chunks
    }
    with open(settings.POLICY_METADATA_PATH, "wb") as f:
        pickle.dump(policy_metadata, f)
    
    logger.info("CREATED POLICY INDEX")
else:
    logger.info("VALID FAISS INDEX FOR POLICY ALREADY EXISTS")