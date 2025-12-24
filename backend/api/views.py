from django.http import JsonResponse
from .tasks import *


# Create your views here.
def health_check(request):
    log_task.delay()
    return JsonResponse({"status": "ok"})
