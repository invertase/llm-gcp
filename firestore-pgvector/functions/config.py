from os import getenv
from dataclasses import dataclass


@dataclass
class Config:
    cloud_sql_instance_name: str = (
        getenv("CLOUD_SQL_INSTANCE_NAME") or "firestore-pgvector-demo"
    )
    collection_name: str = getenv("COLLECTION_NAME") or "pgvector"
    project_id: str = (
        getenv("PROJECT_ID") or getenv("PROJECT") or "invertase--palm-demo"
    )
    location: str = getenv("LOCATION") or "us-central1"
    chunk_size: int = int(getenv("CHUNK_SIZE") or "100")
    cloud_sql_password = getenv("CLOUD_SQL_PASSWORD") or "invertase"
    cloud_sql_db = getenv("CLOUD_SQL_DB") or "postgres"


config = Config()
