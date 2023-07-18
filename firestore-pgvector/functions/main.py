import json
import asyncio
from dataclasses import dataclass
from firebase_admin import firestore, initialize_app


initialize_app()
db = firestore.client()

from firebase_functions import https_fn, tasks_fn
from firebase_functions.options import SupportedRegion, RateLimits
from google.cloud import tasks_v2

# local imports
from utils.firestore import backfill_embeddings_task_handler
from utils.database import vector_search, create_table
from utils.force_sync import force_sync
from config import config


@dataclass
class VectorSearchRequest:
    query: str
    limit: int = 1


def queryindex(request):
    """
    This function is called by the HTTP trigger.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    vector_search_request = VectorSearchRequest(**request.json)

    query = vector_search_request.query
    limit = vector_search_request.limit

    results = force_sync(vector_search)(query, limit)

    return https_fn.Response(
        response=json.dumps(results),
        status=200,
        headers={"Content-Type": "application/json"},
    )


tasks_client = tasks_v2.CloudTasksClient()


# def create_queue():
#     queue_path = tasks_client.queue_path(
#         config.project_id,
#         "us-central1",
#         "backfillembeddingsqueue1",
#     )

#     print("queue_path", queue_path)

#     try:
#         tasks_client.get_queue(name=queue_path)
#         print("Queue already exists")
#         return queue_path
#     except:
#         tasks_client.create_queue(
#             parent=f"projects/{config.project_id}/locations/us-central1",
#             queue={
#                 "name": queue_path,
#                 "rate_limits": {
#                     "max_dispatches_per_second": 10,
#                 },
#             },
#         )
#         from time import sleep

#         sleep(3)

#         return queue_path


def backfilltrigger(req: https_fn.Request):
    # create table in our Cloud SQL database instance, and set up postgresql vector extension.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    force_sync(create_table)()

    document_ids = [doc.id for doc in db.collection("pgvector").list_documents()]

    print("refs data", document_ids)

    if len(document_ids) == 0:
        print("No documents in collection")
        return
    print(f"Found {len(document_ids)} documents in collection")

    # queue_path = create_queue()

    counter = 1
    db.collection("task_collection").document("task_document").set(
        {"total_length": len(document_ids), "processed_length": 0, "status": "PENDING"}
    )

    # batch up the refs into chunks
    chunks = [
        document_ids[x : x + config.chunk_size]
        for x in range(0, len(document_ids), config.chunk_size)
    ]

    for chunk in chunks:
        chunk_document_id = f"chunk_{counter}"
        counter += 1
        document_ids = chunk
        # write chunk to document in task_collection
        db.collection("embeddings").document(chunk_document_id).set(
            {"document_ids": document_ids, "status": "PENDING"}
        )
        # queue a task to process the chunk
        body = {
            "data": {
                "document_ids": document_ids,
                "chunk_document_id": chunk_document_id,
            }
        }

        queue_path = tasks_client.queue_path(
            config.project_id,
            "us-central1",
            "ext-firestore-pgvector-backfillembeddingtask",
        )

        task = tasks_v2.Task(
            http_request={
                "http_method": tasks_v2.HttpMethod.POST,
                "url": req.get_json().get("url"),
                "headers": {
                    "Content-type": "application/json"
                },
                "body": json.dumps(body).encode(),
            }
        )
        print("adding task to queue")
        tasks_client.create_task(parent=queue_path, task=task)
    return "OK"

def backfillembeddingtask(req):
    print("called backfill_embeddings_task")
    
    data = req.get("data")


    chunk_document_id = data["chunk_document_id"]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    force_sync(backfill_embeddings_task_handler)(data)

    print("backfill_embeddings_task_handler finished", data)

    task_doc = (
        db.collection("task_collection").document("task_document").get().to_dict()
    )
    processed_length = task_doc["processed_length"] + len(data["document_ids"])
    status = "PENDING" if processed_length < task_doc["total_length"] else "COMPLETE"

    db.collection("embeddings").document(chunk_document_id).update(
        {"status": "COMPLETE"}
    )
    db.collection("task_collection").document("task_document").update(
        {"processed_length": processed_length, "status": status}
    )
    return "OK"
