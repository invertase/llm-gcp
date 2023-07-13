import json
import asyncio
from dataclasses import dataclass
from firebase_admin import firestore, initialize_app
from firebase_functions import https_fn, firestore_fn
# local imports
from utils.firestore import backfill_embeddings_task_handler
from utils.database import vector_search, create_table
from utils.force_sync import force_sync
from config import config

initialize_app()
db = firestore.client()

@dataclass
class VectorSearchRequest:
    query: str
    limit: int = 1

@https_fn.on_request()
def queryindex(request):
    """
    This function is called by the HTTP trigger.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


    vector_search_request = VectorSearchRequest(**request.json)

    query = vector_search_request.query
    limit = vector_search_request.limit

    results =  force_sync(vector_search)(query, limit)

    return https_fn.Response(
        response=json.dumps(results), status=200, headers={"Content-Type": "application/json"}
    )


def backfilltrigger():

    # create table in our Cloud SQL database instance, and set up postgresql vector extension.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    force_sync(create_table)()

    collection = db.collection(config.collection_name)
    refs = collection.stream()


    if (len(refs) == 0):
        print('No documents in collection')
        return
    print(f"Found {len(refs)} documents in collection")
    


    counter = 1
    db.collection("task_collection").document("task_document").set({
        "total_length": len(refs),
        "processed_length": 0,
        "status": "PENDING"
    })

    # batch up the refs into chunks
    chunks = [refs[x:x+config.chunk_size] for x in range(0, len(refs), config.chunk_size)]

    for chunk in chunks:
        id = f"chunk_{counter}"
        # write chunk to document in task_collection
        db.collection("embeddings").document(id).set({
            "document_ids": [doc.id for doc in chunk],
            "status": "PENDING"
        })

@firestore_fn.on_document_created("embeddings/{document_id}")
def backfill_embeddings_task(change):

    data = change.data()
    document_id = change.document_id

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


    force_sync(backfill_embeddings_task_handler)(data)


    task_doc = db.collection("task_collection").document("task_document").get().to_dict()
    processed_length = task_doc["processed_length"] + len(data["document_ids"])
    status = "PENDING" if processed_length < task_doc["total_length"] else "COMPLETE"

    db.collection("embeddings").document(document_id).update({
            "status": "COMPLETE"
    })
    db.collection("task_collection").document("task_document").update({
        "processed_length": processed_length,
        "status": status
    })


    
    

