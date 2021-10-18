from django.core.management.base import BaseCommand

from places.utils.create_place_entry_from_json import(
    create_place_record_from_github_jsons
)


class Command(BaseCommand):
    help = 'Загрузить локации и фото к ним из json-файлов с GitHub'

    def handle(self, *args, **options):
        owner, repo, folder = options["owner"], options["repo"], options["folder"]
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{folder}'
        create_place_record_from_github_jsons(url)

    def add_arguments(self, parser):
        parser.add_argument('owner', metavar='владелец_репозитория')
        parser.add_argument('repo', metavar='имя_репозитория')
        parser.add_argument('folder', metavar='директория_с_json_файлами')
