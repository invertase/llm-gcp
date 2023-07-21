import json

from google.cloud import tasks_v2

from config import config

tasks_client = tasks_v2.CloudTasksClient()


def backfilltrigger(data):

    body = {
        "data": {
            "foo": "bar",
        }
    }

    queue_path = tasks_client.queue_path(
        config.project_id,
        config.location,
        f"ext-{config.ext_instance_id_string}-backfillembeddingtask",
    )

    task = tasks_v2.Task(
        http_request={
            "http_method": tasks_v2.HttpMethod.POST,
            "url": f"https://{config.location}-{config.project_id}.cloudfunctions.net/ext-{config.ext_instance_id_string}-backfillembeddingtask",
            "headers": {"Content-type": "application/json"},
            "body": json.dumps(body).encode(),
        }
    )
    print("adding task to queue")

    tasks_client.create_task(parent=queue_path, task=task)

    return "OK"


def backfillembeddingtask(req):
    print("called backfill task")
    return "OK"
