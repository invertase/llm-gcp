from typing import List
from dataclasses import dataclass
from vertexai.preview.language_models import TextEmbeddingModel, TextEmbedding

COLLECTION_NAME = "pgvector"

DIMENSION = 768

from firebase_admin import firestore, initialize_app

initialize_app()

db = firestore.client()

def backfill_embeddings_task(data):
    """
    This function is called by the Cloud Task.
    """
    id = data.get("id")
    collection_name = data.get("collection_name")
    document_ids = data.get("document_ids")

    if (id is None or collection_name is None or document_ids is None):
        print("Missing required data")
        raise Exception("Missing required data")

    # TODO
    task_ref = "task_reference"
    
    documents = get_documents(document_ids)

    embeddings = get_embeddings(documents)

    # print(embeddings)
    return embeddings

    # upload_embeddings(embeddings)

    # get tasksDoc from firestore, update it with count of documents processed

@dataclass
class Document:
    id: str
    content: dict

@dataclass
class Vector:
    id: str
    values: List[float]

def get_documents(document_ids: List[str]) -> List[Document]:
    """Get documents from Firestore."""
    return [db.collection(COLLECTION_NAME).document(id).get().to_dict() for id in document_ids]

def get_embeddings(documents: List[Document]) -> List[Vector]:
    """Text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

    inputs = [extract_embedding_input(d) for d in documents]

    embeddings = model.get_embeddings(inputs)
    ids = [d["id"] for d in documents]

    return [Vector(id=id, values=e.values) for id, e in zip(ids, embeddings)]


def extract_embedding_input(document: Document) -> str:
    """Extracts the text from a document."""

    # TODO: allow configuration of which field(s) to use
    return document["title"]


# embeddings = backfill_embeddings_task({
#     "id": "task_id",
#     "collection_name": "pgvector",
#     "document_ids": ["1", "2", "3", "4", "5"]
# })


# upload embeddings to cloud sql

import asyncio
import asyncpg
from google.cloud.sql.connector import Connector
from pgvector.asyncpg import register_vector
import numpy as np

async def upload_embeddings():
    loop = asyncio.get_running_loop()

    async with Connector(loop=loop) as connector:
        # Create connection to Cloud SQL PostgreSQL database
        conn: asyncpg.Connection = await connector.connect_async(
            f"invertase--palm-demo:us-central1:firestore-pgvector-demo",
            "asyncpg",
            user="postgres",
            password="invertase",
            db = f"postgres"
        )

        # conn.execute("CREATE TABLE IF NOT EXISTS embeddings (id VARCHAR(1024) PRIMARY KEY, values REAL[]);")
        print("registering vector")

        await register_vector(conn)

        print("registered vector")

        query_plaintext = "backpack"

        model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

        query_embeddings = model.get_embeddings([query_plaintext])

        arr = np.array(query_embeddings[0].values)



        result = await conn.fetch('SELECT id FROM embeddings ORDER BY embedding <-> $1 LIMIT 1', arr)

        print('result:',result)


        # print(len(embeddings))

        # for embedding in embeddings:
        #     await conn.execute("INSERT INTO embeddings (id, embedding) VALUES ($1, $2);", embedding.id, np.array(embedding.values))
        #     print(f"inserted {embedding.id}")


async def main():
    await upload_embeddings()

if __name__ == "__main__":
    asyncio.run(main())