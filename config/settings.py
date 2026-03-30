# Data files
ECOMMERCE_DATA_FILE_PATH: str = "./data/ecommerce_data.csv"
POLICY_DATA_FILE_PATH: str = "./data/ecommerce_policies.pdf"

# Generated files
GENERATED_DIR: str = "./generated"
ECOMMERCE_DB_PATH: str = "./generated/database.db"
POLICY_FAISS_INDEX_PATH: str = "./generated/policy_index.faiss"
POLICY_METADATA_PATH: str = "./generated/policy_metadata.pkl"

# Application config
# EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large-instruct"
EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
CHAT_SESSION_TTL: int = 1800 # 30 minutes
MAX_CHAT_SESSION_MESSAGES: int = 500