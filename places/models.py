from pathlib import Path

from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):

    class PublicationStatus(models.TextChoices):
        DRAFT = 'D', 'Черновик'
        PUBLISHED = 'P', 'Опубликован'

    title = models.CharField(max_length=200, verbose_name='Название локации')
    slug = models.SlugField(unique=True)
    description_short = models.TextField(blank=True,
                                         verbose_name='Короткое описание')
    description_long = HTMLField(blank=True,
                                 verbose_name='Подробное описание')
    longitude = models.FloatField(verbose_name='Долгота',
                                  blank=True,
                                  null=True)
    latitude = models.FloatField(verbose_name='Широта',
                                 null=True,
                                 blank=True)
    pub_status = models.CharField(db_index=True,
                                  max_length=1,
                                  choices=PublicationStatus.choices,
                                  default=PublicationStatus.DRAFT,
                                  verbose_name='Статус публикации')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.title


def get_upload_path(instance, filename):
    return Path(instance.place.slug) / filename


class Image(models.Model):
    priority = models.PositiveIntegerField(db_index=True, blank=True, default=0)
    place = models.ForeignKey(to=Place,
                              on_delete=models.CASCADE,
                              related_name='images')
    image = models.ImageField(upload_to=get_upload_path,
                              verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ('priority', )

    def __str__(self):
        return f'{self.pk} {self.place}'
