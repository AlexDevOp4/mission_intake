import uuid
import os
import requests
import logging

from requests.exceptions import RequestException
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="api.tasks.log_task")
def log_task():
    my_uuid = uuid.uuid4()
    print(f"Task logged! id {my_uuid}")


@shared_task(name="api.tasks.audit_log")
def audit_log(event_type, message, request_id, source):
    from api.models import AuditLog

    logger.info("audit_log_created", extra={"request_id": request_id})

    new_audit_log = AuditLog.objects.create(
        event_type=event_type, message=message, request_id=request_id, source=source
    )

    index_audit_log.delay(new_audit_log.id)


@shared_task(
    name="api.tasks.index_audit_log",
    autoretry_for=(RequestException,),
    max_retries=7,
    retry_backoff=True,
    retry_jitter=True,
)
def index_audit_log(audit_log_id):
    from api.models import AuditLog

    # Made audit_log the id of the Audit so there will be no duplicate, stable and deterministic.
    audit_log = AuditLog.objects.get(id=audit_log_id)
    logger.info(f"indexing_audit_log", extra={"request_id": audit_log.request_id})
    SOLR_URL = os.getenv("SOLR_URL", "http://solr:8983/solr/audit_logs")
    print(f"Indexing audit_log_id={audit_log_id} into Solr")
    document = {
        "id": audit_log_id,
        "event_type": audit_log.event_type,
        "message": audit_log.message,
        "request_id": audit_log.request_id,
        "source": audit_log.source,
        "created_at": audit_log.created_at.isoformat(),
    }

    response = requests.post(SOLR_URL, json=[document])
    response.raise_for_status()
    return response.json()
