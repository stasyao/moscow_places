from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создать учётку администратора для работы с локациями '

    def handle(self, *args, **options):
        username, password = options['username'], options['password']
        admin = get_user_model().objects.create_user(username, password=password, is_staff=True)
        permissions = admin.user_permissions.model.objects.filter(
            codename__in=['add_place', 'change_place', 'delete_place',
                          'add_image', 'change_image', 'delete_image']
        ).values_list('pk', flat=True)
        admin.user_permissions.set(permissions)

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('password')
