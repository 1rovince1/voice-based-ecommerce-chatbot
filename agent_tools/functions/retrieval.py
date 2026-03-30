import logging
import pickle
import sqlite3

import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

from config import settings

logger = logging.getLogger(__name__)


logger.info("Loading embedding model...")
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
logger.info("Loaded embedding model")


# SQL tool for csv DB query
def database_query_tool(query: str):
    """Run a SQL SELECT query on SQLite ecommerce database and return the results."""
    try:
        connection = sqlite3.connect(settings.ECOMMERCE_DB_PATH)
        result = pd.read_sql_query(query, connection).to_dict(orient="records")
        connection.close()
        return result
    
    except Exception as e:
        logger.exception(f"Error in running SQL query: {str(e)}")
        raise e
    

# Semantic search retrieval tool
def policy_query_tool(query: str) -> list[str]:
    """Fetch relevant information chunks from policy document"""
    try:
        policy_index = faiss.read_index(settings.POLICY_FAISS_INDEX_PATH)
        with open(settings.POLICY_METADATA_PATH, "rb") as f:
            policy_metadata = pickle.load(f)
        content_chunks = policy_metadata.get("content_chunks")
        
        query_embedding = embedding_model.encode([query])
        D, I = policy_index.search(query_embedding, 10)
        return [f"{i}: {content_chunks[i]}" for i in I[0]]
    
    except Exception as e:
        logger.exception(f"Error in running policy query: {str(e)}")
        raise e