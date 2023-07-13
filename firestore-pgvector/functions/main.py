from typing import List
from dataclasses import dataclass
from utils.firestore import get_datapoints, get_collection_ids, backfill_embeddings_task
from utils.database import upload_embeddings, vector_search, create_table
from utils.llm import assign_embeddings
from firebase_functions import https_fn
import asyncio
import functools
import json

COLLECTION_NAME = "pgvector"
DIMENSION = 768


@dataclass
class VectorSearchRequest:
    query: str
    limit: int = 1


def force_sync(fn):
    '''
    turn an async function to sync function
    '''
    import asyncio

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper

@https_fn.on_request()
def http_vector_search(request):
    """
    This function is called by the HTTP trigger.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


    vector_search_request = VectorSearchRequest(**request.json)

    query = vector_search_request.query
    limit = vector_search_request.limit

    results =  force_sync(vector_search)(query, limit)

    print("RESULTS", [json.dumps(r) for r in results])

    return https_fn.Response(
        response=json.dumps(results), status=200, headers={"Content-Type": "application/json"}
    )

import argparse


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--collection_name", type=str, help="collection name")
    args = parser.parse_args()
    config = vars(args)

    await create_table()

    collection_name = config["collection_name"]
    document_ids = get_collection_ids(collection_name)

    print('document_ids', document_ids)

    await backfill_embeddings_task({
        "id": "task_id",
        "collection_name": collection_name,
        "document_ids": document_ids
    })

if __name__ == "__main__":
    asyncio.run(main())