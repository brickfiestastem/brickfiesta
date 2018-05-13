from django.db import models
import uuid
from django.contrib.auth.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class Article(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField()

    class Meta:
        ordering = ['-created', 'title']

    def __str__(self):
        return self.title


class QuestionAnswer(BaseModel):
    QUESTION_TYPE = (
        ('convention', 'Fan Convention'),
        ('public', 'Public Exhibition'),
        ('vendor', 'Vendor'),
        ('sponsor', 'Sponsor'),
    )
    question_type = models.CharField(
        max_length=64, blank=False, choices=QUESTION_TYPE, default='convention')
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        ordering = ['question_type', 'question']
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question
