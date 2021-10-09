from django.core.management.base import BaseCommand

from places.utils import github_jsons_to_place


class Command(BaseCommand):
    help = ('Загрузить локации и фото к ним из json-файлов с GitHub'
            'Три аргумента: 1) владелец репозитория; 2) имя репозитория'
            '3) директория в репозитории с json-файлами')

    def handle(self, *args, **options):
        user = options["repo_owner"][0]
        repo = options["repo"][0]
        folder = options["folder"][0]
        url = f'https://api.github.com/repos/{user}/{repo}/contents/{folder}'
        github_jsons_to_place(url)

    def add_arguments(self, parser):
        parser.add_argument(nargs=1, type=str, dest='repo_owner')
        parser.add_argument(nargs=1, type=str, dest='repo')
        parser.add_argument(nargs=1, type=str, dest='folder')
