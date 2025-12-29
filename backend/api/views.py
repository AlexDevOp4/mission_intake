import logging
import uuid
from django.http import JsonResponse
from .tasks import audit_log
from api.health.database import check_database_health

logger = logging.getLogger(__name__)


def health_check(request):
    uuid_object = uuid.uuid4()
    request_id = str(uuid_object)
    logger.info("health_check_called", extra={"request_id": request_id})
    
    if check_database_health():
        return JsonResponse({"status": "ok", "request_id": request_id})
    return JsonResponse({"status": "unhealthy"}, status=503)
