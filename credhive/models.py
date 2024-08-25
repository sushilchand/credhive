import uuid

from django.db import models


# Base Model to auto generate required fields
class TimestampModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
