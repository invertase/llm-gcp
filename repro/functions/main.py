import os
import json
import requests

from google.cloud import tasks_v2

from config import config

tasks_client = tasks_v2.CloudTasksClient()

import requests

GOOGLE_METADATA_SERVICE_IDENTITY_PATH = 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity'

def get_id_token(audience):
    print("get_id_token >>>>", GOOGLE_METADATA_SERVICE_IDENTITY_PATH, audience)
    headers = {'Metadata-Flavor': 'Google'}
    params = {'audience': audience}
    response = requests.get(GOOGLE_METADATA_SERVICE_IDENTITY_PATH, headers=headers, params=params)

    print("response >>>>", response.status_code, response.text)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Request failed with status {response.status_code}")


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

    URL = f"https://{config.location}-{config.project_id}.cloudfunctions.net/ext-{config.ext_instance_id_string}-backfillembeddingtask"

    task = tasks_v2.Task(
        http_request=tasks_v2.HttpRequest(
            http_method=tasks_v2.HttpMethod.POST,
            url=URL,
            headers={"Content-type": "application/json", "Authorization": f"Bearer {get_id_token(URL)}"},
            body=json.dumps(body).encode(),
       )
    )
    
    print("adding task to queue")

    tasks_client.create_task(parent=queue_path, task=task)

    return "OK"


def backfillembeddingtask(req):
    print("called backfill task")
    return "OK"
