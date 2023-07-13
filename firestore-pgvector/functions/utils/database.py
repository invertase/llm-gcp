import asyncio
import asyncpg
from google.cloud.sql.connector import Connector
from pgvector.asyncpg import register_vector
import numpy as np
from utils.llm import model
from utils.datapoint import Datapoint
from typing import List

async def upload_embeddings(datapoints: List[Datapoint]):
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

        # conn.execute("CREATE TABLE IF NOT EXISTS embeddings (id VARCHAR(1024) PRIMARY KEY, content VARCHAR(1024), embedding vector(768));")


        #  TODO: can we move this whole connection logic out so that it's not called every time?
        await register_vector(conn)

        # print(len(embeddings))

        for datapoint in datapoints:
            # TODO: handle clashing ids
            await conn.execute("INSERT INTO embeddings (id, content, embedding) VALUES ($1, $2, $3);", datapoint.id, datapoint.content, datapoint.embedding)
            # print(f"inserted {datapoint.id}")
        print("inserted datapoints", [d.id for d in datapoints])


async def vector_search(plaintext_query: str, limit: int = 1):
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

        await register_vector(conn)

        # model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

        embedded_query = model.get_embeddings([plaintext_query])

        arr = np.array(embedded_query[0].values)

        result = await conn.fetch('SELECT id FROM embeddings ORDER BY embedding <-> $1 LIMIT $2', arr, str(limit))

        print('result',result)

        return result