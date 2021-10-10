from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('Создать учётку администратора для работы с локациями'
            'Два аргумента: 1) юзернейм; 2) пароль')

    def handle(self, *args, **options):
        username = options['username'][0]
        password = options['password'][0]
        admin = get_user_model().objects.create_user(username, password=password, is_staff=True)
        perm_list = admin.user_permissions.model.objects.filter(
            codename__in=['add_place', 'change_place', 'delete_place',
                          'add_image', 'change_image', 'delete_image']
        )
        admin.user_permissions.set([perm.pk for perm in perm_list])

    def add_arguments(self, parser):
        parser.add_argument(nargs=1, type=str, dest='username')
        parser.add_argument(nargs=1, type=str, dest='password')
