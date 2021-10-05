from django.db import models
from django.db.models.fields.json import JSONField


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
    pass
