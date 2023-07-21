from firebase_admin import firestore, initialize_app
from typing import List
import asyncio
from utils.datapoint import Datapoint
from dataclasses import dataclass
from utils.llm import assign_embeddings
from utils.database import upload_embeddings
from config import config

# initialize_app()

db = firestore.client()


def get_collection_ids(collection_name: str) -> List[str]:
    """Get all document ids from a collection."""

    print(f"Getting all document ids from collection {collection_name}")

    return [doc.id for doc in db.collection(collection_name).stream()]


def get_doc(document_id: str) -> dict:
    """Get document from Firestore."""

    print(f"Getting document {document_id} from Firestore")

    return db.collection(config.collection_name).document(document_id).get().to_dict()


def concatentate_fields(doc_dict) -> str:
    """Concatenate fields from document."""
    fields = config.fields
    return " ".join([doc_dict[field] for field in fields])

def extract_embedding_input(doc_dict) -> str:
    """Extract embedding input from document fields."""
    return concatentate_fields(doc_dict)


def get_datapoints(document_ids: List[str]) -> List[Datapoint]:
    """Get documents from Firestore - asynchronously."""
    return [
        Datapoint(id=doc_id, content=extract_embedding_input(get_doc(doc_id)))
        for doc_id in document_ids
    ]


async def backfill_embeddings_chunk(document_ids: List[str]):
    """Get documents from Firestore - asynchronously."""
    datapoints = get_datapoints(document_ids)
    assign_embeddings(datapoints)
    await upload_embeddings(datapoints)


@dataclass
class BackfillTaskRequest:
    chunk_document_id: str
    # collection_name: str
    document_ids: List[str]


async def backfill_embeddings_task_handler(data):
    """
    This function is called by the Cloud Task.
    Assume document_ids come in as a list of strings of length 100.
    Assumes table etc has been set up.
    """

    backfill_task = BackfillTaskRequest(**data)

    # collection_name = backfill_task.collection_name
    document_ids = backfill_task.document_ids

    futures = [
        backfill_embeddings_chunk(document_ids[i : i + 5])
        for i in range(0, len(document_ids), 5)
    ]

    await asyncio.gather(*futures)

    return "Done!"
