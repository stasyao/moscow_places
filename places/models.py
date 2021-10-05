from django.db import models
from django.db.models.fields.json import JSONField

from config.settings import MEDIA_ROOT

class Place(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description_short = models.CharField(max_length=300, unique=True)
    description_long = models.TextField(unique=True)
    coordinates = JSONField(default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'description_short', 'description_long'],
                                    name='unique_places')
        ]
        ordering = ('title',)

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    description = models.CharField(max_length=100)
    priority = models.PositiveIntegerField(unique=True)
    image = models.ImageField(upload_to=MEDIA_ROOT)
    location = models.ForeignKey(to=Place, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.pk} {self.location}'
