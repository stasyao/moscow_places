from django.core.management.base import BaseCommand
import requests

from places.utils import json_url_to_place


class Command(BaseCommand):
    help = ('Загрузить локации и фото к ним из json-файла. '
            'Один аргумент: URL json файла')

    def handle(self, *args, **options):
        path = options['path_to_json'][0]
        json_url_to_place(path)

    def add_arguments(self, parser):
        parser.add_argument(nargs=1, type=str, dest='path_to_json')
