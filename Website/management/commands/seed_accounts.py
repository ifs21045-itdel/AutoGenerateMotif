# myapp/management/commands/seed_accounts.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed database with specified test accounts'

    def handle(self, *args, **kwargs):
        users = [
            {
                'username': 'ditenun.admin',
                'email': 'ditenun01@gmail.com',
                'password': 'diTenun0999',
                'is_staff': 1, # Note: use 1 for True
                'is_active': 1, # Note: use 0 for False
                'is_superuser': 1
            },
            {
                'username': 'hedrin99',
                'email': 'sitorushedrin@gmail.com',
                'password': 'admin29902',
                'is_staff': 1,
                'is_active': 1,
                'is_superuser': 1
            },
            {
                'username': 'guest',
                'email': 'guest@gmail.com',
                'password': 'guest2024',
                'is_staff': 1,
                'is_active': 1,
                'is_superuser': 1
            }
        ]
        
        for user_data in users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'], 
                    email=user_data['email'], 
                    password=user_data['password']
                )
                user.is_staff = user_data['is_staff']
                user.is_active = user_data['is_active']
                user.is_superuser = user_data['is_superuser']
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created user {user_data["username"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {user_data["username"]} already exists'))
