import uuid
from celery import shared_task


@shared_task
def log_task():
    my_uuid = uuid.uuid4()
    print(f"Task logged! id {my_uuid}")
