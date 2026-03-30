import logging
import pandas as pd
import sqlite3
from sentence_transformers import SentenceTransformer
import pickle
import faiss

from config import config

logger = logging.getLogger(__name__)


logger.info("Loading embedding model...")
embedding_model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)
logger.info("Loaded embedding model")

# SQL tool for csv DB query
def sql_tool(query: str):
    """Run a SQL SELECT query on a SQLite database and return the results."""
    try:
        connection = sqlite3.connect(config.ECOMMERCE_DB_PATH)
        result = pd.read_sql_query(query, connection).to_dict(orient="records")
        connection.close()
        return result
    except Exception as e:
        logger.exception(f"Error in running SQL query: {str(e)}")
        return e
    

def policy_query_tool(query: str):
    """Fetch relevant information chunks from policy document"""
    try:
        policy_index = faiss.read_index(config.POLICY_FAISS_INDEX_PATH)
        with open(config.POLICY_METADATA_PATH, "rb") as f:
            policy_metadata = pickle.load(f)
        content_chunks = policy_metadata.get("content_chunks")
        
        query_embedding = embedding_model.encode([query])
        D, I = policy_index.search(query_embedding, 10)
        return [f"{i}: {content_chunks[i]}" for i in I[0]]
    except Exception as e:
        logger.exception(f"Error in running policy query: {str(e)}")
        return e