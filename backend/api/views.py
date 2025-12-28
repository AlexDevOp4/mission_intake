import logging
import uuid
from django.http import JsonResponse
from .tasks import audit_log

logger = logging.getLogger(__name__)


# Create your views here.
def health_check(request):
    uuid_object = uuid.uuid4()
    request_id = str(uuid_object)
    logger.info("health_check_called", extra={"request_id" : request_id})
    
    source = "web"
    audit_log.delay(
        "HEALTH_CHECK", "Health check endpoint accessed via GET", request_id, source
    )
    return JsonResponse({"status": "ok", "request_id": request_id})
