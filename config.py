class Config():
    # Data files
    ECOMMERCE_DATA_FILE_PATH = "./data/ecommerce_data.csv"
    POLICY_DATA_FILE_PATH = "./data/ecommerce_policies.pdf"

    # Generated files
    GENERATED_DIR = "./generated"
    ECOMMERCE_DB_PATH = "./generated/database.db"
    POLICY_FAISS_INDEX_PATH = "./generated/policy_index.faiss"
    POLICY_METADATA_PATH = "./generated/policy_metadata.pkl"

    # Application config
    EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large-instruct"
    
config = Config()