from django.db import models
from django.contrib.auth.models import User
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Article(BaseModel):
    user = models.ForeignKey(User, on_delete=None)
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField()


class QuestionAnswer(BaseModel):
    QUESTION_TYPE = (
        ('vendor', 'Vendor'),
    )
    question_type = models.CharField(max_length=64, blank=False)
    question = models.TextField()
    answer = models.TextField()
