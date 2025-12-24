import logging
from django.http import JsonResponse
from .tasks import audit_log

logger = logging.getLogger(__name__)

# Create your views here.
def health_check(request):
    audit_log.delay("HEALTH_CHECK", "Health check endpoint accessed via GET")
    return JsonResponse({"status": "ok"})
