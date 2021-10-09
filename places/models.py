from pathlib import Path

from django.db import models
from django.db.models.fields.json import JSONField
from slugify import slugify
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True)
    description_short = models.CharField(max_length=300, unique=True)
    description_long = HTMLField()
    coordinates = JSONField(default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'description_short', 'description_long'],
                name='unique_places'
            )
        ]
        ordering = ('title',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Image(models.Model):
    priority = models.PositiveIntegerField(default=0)
    location = models.ForeignKey(to=Place, on_delete=models.CASCADE)

    def get_upload_path(instance, filename):
        return Path(instance.location.slug) / filename

    image = models.ImageField(upload_to=get_upload_path)

    class Meta:
        ordering = ('priority',)

    def __str__(self) -> str:
        return f'{self.pk} {self.location}'
