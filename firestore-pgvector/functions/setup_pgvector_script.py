import asyncio
import argparse
from utils.database import create_table
from utils.firestore import get_collection_ids, backfill_embeddings_task

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