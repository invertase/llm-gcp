from firebase_admin import firestore, initialize_app
from typing import List
import asyncio
from utils.datapoint import Datapoint

COLLECTION_NAME = "pgvector"

initialize_app()

db = firestore.client()

def get_doc(document_id: str) -> dict:
    """Get document from Firestore."""

    print(f"Getting document {document_id} from Firestore")

    return db.collection(COLLECTION_NAME).document(document_id).get().to_dict()

def extract_embedding_input(doc_dict) -> str:
    """Extract embedding input from document fields."""
    # TODO: add support for multiple fields/configurable fields
    return doc_dict["title"]

def get_datapoints(document_ids: List[str]) -> List[Datapoint]:
    """Get documents from Firestore - asynchronously."""
    return [Datapoint(id=doc_id, content=extract_embedding_input(get_doc(doc_id))) for doc_id in document_ids]
