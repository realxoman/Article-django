from django.db import models


class BaseModel(models.Model):
    """
    Base Model to inherit in each model these fields may be required.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
