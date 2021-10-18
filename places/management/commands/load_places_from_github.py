from urllib.parse import urlparse

from django.core.management.base import BaseCommand

from places.utils.create_place_entry_from_json import (
    create_place_record_from_github_jsons
)


class Command(BaseCommand):
    help = 'Загрузить локации и фото к ним из json-файлов с GitHub'

    def handle(self, *args, **options):
        path_to_folder = urlparse(options['github_url']).path
        owner, repo, *_, folder = list(filter(None, path_to_folder.split('/')))
        download_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{folder}'
        create_place_record_from_github_jsons(download_url)

    def add_arguments(self, parser):
        parser.add_argument('github_url')
