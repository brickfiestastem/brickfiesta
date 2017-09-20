from django.db import models
import uuid

class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True

class Category(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='Name', unique=True, max_length=64)
    description = models.TextField(verbose_name='Description')
    age_limit_min = models.IntegerField(verbose_name='Minimum Age Limit')
    age_limit_max = models.IntegerField(verbose_name='Maximum Age Limit')

    def __str__(self):
        return self.name