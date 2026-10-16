import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Ensures default and secondary superadmin users exist in the production database (Railway/Deployment).'

    def handle(self, *args, **options):
        admin_accounts = [
            {
                'username': os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin'),
                'email': os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@passli.dev'),
                'password': os.getenv('DJANGO_SUPERUSER_PASSWORD', 'PassliAdminDefault2026!'),
            },
            {
                'username': os.getenv('DJANGO_SECONDARY_SUPERUSER_USERNAME', 'superadmin'),
                'email': os.getenv('DJANGO_SECONDARY_SUPERUSER_EMAIL', 'superadmin@passli.dev'),
                'password': os.getenv('DJANGO_SECONDARY_SUPERUSER_PASSWORD', 'PassliSuperAdmin2026!'),
            },
            {
                'username': 'alinawazcode',
                'email': 'alinawaz@passli.dev',
                'password': os.getenv('DJANGO_ALINAWAZ_PASSWORD', 'PassliAdminDefault2026!'),
            },
        ]

        for account in admin_accounts:
            user, created = User.objects.get_or_create(
                username=account['username'],
                defaults={'email': account['email']}
            )

            user.set_password(account['password'])
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            if account['email']:
                user.email = account['email']
            user.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"Superadmin '{account['username']}' created successfully."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Superadmin '{account['username']}' credentials synchronized."))

