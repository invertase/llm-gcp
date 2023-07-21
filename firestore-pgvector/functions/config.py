from os import getenv
from dataclasses import dataclass


@dataclass
class Config:
    cloud_sql_instance_name: str = (
        getenv("CLOUD_SQL_INSTANCE_NAME")
    )
    collection_name: str = getenv("COLLECTION_NAME")
    project_id: str = (
        getenv("PROJECT_ID") or getenv("PROJECT")
    )
    location: str = getenv("LOCATION")
    chunk_size: int = int(getenv("CHUNK_SIZE") or "100")
    cloud_sql_password = getenv("CLOUD_SQL_PASSWORD")
    cloud_sql_db = getenv("CLOUD_SQL_DB")
    ext_instance_id = getenv("EXT_INSTANCE_ID"),
    # get first element of tuple:
    ext_instance_id_string = getenv("EXT_INSTANCE_ID")[0] if isinstance(getenv("EXT_INSTANCE_ID"), tuple) else getenv("EXT_INSTANCE_ID")
    task_collection_name = getenv("TASK_COLLECTION_NAME")
    fields = getenv("FIELDS").split(",")
    cloud_sql_table_name = getenv("CLOUD_SQL_TABLE_NAME")


config = Config()
