import json
import asyncio
from dataclasses import dataclass
from firebase_functions import https_fn
# local imports
from utils.database import vector_search
from utils.force_sync import force_sync

@dataclass
class VectorSearchRequest:
    query: str
    limit: int = 1


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

    return https_fn.Response(
        response=json.dumps(results), status=200, headers={"Content-Type": "application/json"}
    )

