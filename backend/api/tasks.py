import uuid
from celery import shared_task


@shared_task(name="api.tasks.log_task")
def log_task():
    my_uuid = uuid.uuid4()
    print(f"Task logged! id {my_uuid}")


@shared_task(name="api.tasks.audit_log")
def audit_log(event_type, message, request_id, source):
    from api.models import AuditLog

    new_audit_log = AuditLog.objects.create(
        event_type=event_type, message=message, request_id=request_id, source=source
    )

    index_audit_log.delay(new_audit_log.id)


@shared_task(name="api.tasks.index_audit_log")
def index_audit_log(audit_log_id):
    from api.models import AuditLog

    audit_log = AuditLog.objects.get(id=audit_log_id)
    document = {
        "id": audit_log_id,
        "event_type": audit_log.event_type,
        "message": audit_log.message,
        "request_id": audit_log.request_id,
        "source": audit_log.source,
        "created_at": audit_log.created_at.isoformat(),
    }
