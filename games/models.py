import uuid
from random import randint

from django.db import models
from django.db.models.aggregates import Count

from afol.models import Fan
from event.models import Event, Schedule


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        verbose_name='Last Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class DoorPrizeWinner(BaseModel):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return "{} won at {}".format(self.fan, self.event)

    class Meta:
        ordering = ('-created', '-event')
        unique_together = ('fan', 'event')


class DoorPrizePoolManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class DoorPrizePool(BaseModel):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)

    def __str__(self):
        return "{} is in the pool {}".format(self.fan, self.schedule)

    class Meta:
        unique_together = ('fan', 'schedule')
