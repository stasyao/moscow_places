from django.core.management.base import BaseCommand

from places.utils.create_place_entry_from_json import json_url_to_place


class Command(BaseCommand):
    help = 'Загрузить локации и фото к ним из json-файла'

    def handle(self, *args, **options):
        json_url_to_place(options['path_to_json_file'])

    def add_arguments(self, parser):
        parser.add_argument('path_to_json_file')
