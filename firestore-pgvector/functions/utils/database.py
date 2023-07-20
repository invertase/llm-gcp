import asyncio
from asyncio.events import AbstractEventLoop
import asyncpg
from google.cloud.sql.connector import Connector
from pgvector.asyncpg import register_vector
import numpy as np
from utils.llm import model
from utils.datapoint import Datapoint
from typing import List, Union
from config import config

connection_name = (
    f"{config.project_id}:{config.location}:{config.cloud_sql_instance_name}"
)


def catch_exception(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("error", e)

    return inner


async def attempt_execution(conn: asyncpg.Connection, sql, just_fetch: bool = False):
    method = conn.fetch if just_fetch else conn.execute
    if isinstance(sql, list):
        return await catch_exception(method)(*sql)
    else:
        return await catch_exception(method)(sql)


async def run_with_connector(
    sql_steps: List[Union[str, List[str]]],
    should_register_vector: bool = False,
    just_fetch: bool = False,
):
    loop = asyncio.get_running_loop()
    async with Connector(loop=loop) as connector:
        conn: asyncpg.Connection = await connector.connect_async(
            connection_name,
            "asyncpg",
            user="postgres",
            password=config.cloud_sql_password,
            db=config.cloud_sql_db,
        )

        if should_register_vector:
            await register_vector(conn)

        result = [await attempt_execution(conn, sql, just_fetch) for sql in sql_steps]

        # await connector.close()

        return result


async def create_table():
    res = await run_with_connector(
        [
            "CREATE EXTENSION IF NOT EXISTS vector;",
            "CREATE TABLE IF NOT EXISTS embeddings (id VARCHAR(1024) PRIMARY KEY, content VARCHAR(1024), embedding vector(768));",
        ]
    )
    return res


async def upload_embeddings(datapoints: List[Datapoint]):
    sql_steps = [
        [
            "INSERT INTO embeddings (id, content, embedding) VALUES ($1, $2, $3) ON CONFLICT (id) DO NOTHING;",
            datapoint.id,
            datapoint.content,
            datapoint.embedding,
        ]
        for datapoint in datapoints
    ]
    await run_with_connector(sql_steps, should_register_vector=True)
    print("inserted datapoints", [d.id for d in datapoints])


async def vector_search(plaintext_query: str, limit: int = 1):
    embedded_query = model.get_embeddings([plaintext_query])

    embedding_values = np.array(embedded_query[0].values)

    result = await run_with_connector(
        [
            [
                "SELECT id,content FROM embeddings ORDER BY embedding <-> $1 LIMIT $2",
                embedding_values,
                limit,
            ]
        ],
        should_register_vector=True,
        just_fetch=True,
    )

    return [dict(row) for row in result]
