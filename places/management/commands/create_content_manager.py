from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('Создать контент-менеджера в составе группы с правами '
            'для работы с локациями')

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('password')

    def handle(self, *args, **options):
        content_managers, created = Group.objects.get_or_create(
            name='content_managers'
        )
        if created:
            permissions = Permission.objects.filter(
                content_type__app_label='places'
            ).values_list('pk', flat=True)
            content_managers.permissions.set(permissions)
        content_manager = get_user_model().objects.create_user(
            options['username'],
            password=options['password'],
            is_staff=True
        )
        content_manager.groups.add(content_managers)
