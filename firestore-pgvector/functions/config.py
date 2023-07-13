from os import getenv
from dataclasses import dataclass
from typing import Optional


default_instance_id = "firestore-pgvector"
default_project = "invertase--palm-demo"

@dataclass
class Config:
    instance_id: str = getenv("EXT_INSTANCE_ID") or default_instance_id
    collection_name: str = getenv("COLLECTION_NAME") or "pgvector"
    project_id: str = getenv("PROJECT_ID") or getenv("PROJECT") or default_project
    location: str = getenv("LOCATION") or "us-central-1"


config = Config()