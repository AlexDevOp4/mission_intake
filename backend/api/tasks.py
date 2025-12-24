import uuid
from celery import shared_task


@shared_task(name="api.tasks.log_task")
def log_task():
    my_uuid = uuid.uuid4()
    print(f"Task logged! id {my_uuid}")
    
@shared_task(name="api.tasks.audit_log")
def audit_log(event_type, message, request_id, source):
    from api.models import AuditLog
    AuditLog.objects.create(event_type=event_type, message=message, request_id=request_id, source=source)
    
