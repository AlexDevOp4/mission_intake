from django.db import models

# Create your models here.
class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_type = models.CharField(max_length=64)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)