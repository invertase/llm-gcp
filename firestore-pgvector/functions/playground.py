from google.cloud import tasks_v2

tasks_client = tasks_v2.CloudTasksClient()

queue_path = tasks_client.queue_path(
    "invertase--palm-demo",
    "us-central1",
    "test",
)

tasks_client.create_queue(
    parent=f"projects/invertase--palm-demo/locations/us-central1",
    queue={
        "name": queue_path,
        "rate_limits": {
            "max_dispatches_per_second": 10,
        },
    },
)


queue = tasks_client.get_queue(name=queue_path)

print(queue)

# queues = tasks_client.list_queues(parent=f"projects/invertase--palm-demo/locations/us-central1")
