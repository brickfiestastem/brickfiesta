import uuid

from django.db import models

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
        unique_together = ('fan', 'event')


class DoorPrizePool(BaseModel):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)

    def __str__(self):
        return "{} is in the pool {}".format(self.fan, self.schedule)

    class Meta:
        unique_together = ('fan', 'schedule')
