from typing import List
from dataclasses import dataclass
from utils.firestore import get_datapoints
from utils.database import upload_embeddings
from utils.llm import assign_embeddings
import asyncio

COLLECTION_NAME = "pgvector"

DIMENSION = 768





@dataclass
class BackfillTaskRequest:
    id: str
    collection_name: str
    document_ids: List[str]


async def backfill_embeddings_chunk(document_ids: List[str]):
    """Get documents from Firestore - asynchronously."""
    datapoints = get_datapoints(document_ids)
    assign_embeddings(datapoints)
    await upload_embeddings(datapoints)


async def backfill_embeddings_task(data):
    """
    This function is called by the Cloud Task.
    Assume document_ids come in as a list of strings of length 100.
    Assumes table etc has been set up.
    """

    backfill_task = BackfillTaskRequest(**data)

    id = backfill_task.id
    collection_name = backfill_task.collection_name
    document_ids = backfill_task.document_ids

    # TODO
    # task_ref = "task_reference"

    print("DOC IDS",document_ids)

    futures = [backfill_embeddings_chunk(document_ids[i:i+5]) for i in range(0, len(document_ids), 5)]

    await asyncio.gather(*futures)

    return "Done!"


async def main():
    await backfill_embeddings_task({
        "id": "task_id",
        "collection_name": "pgvector",
        "document_ids": ["6", "7", "8", "9", "10","11"]
    })

if __name__ == "__main__":
    asyncio.run(main())