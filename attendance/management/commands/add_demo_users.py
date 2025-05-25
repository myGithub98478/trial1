from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from attendance.models import UserProfile

class Command(BaseCommand):
    help = 'Create or update demo users (admin, teacher, student) with specified credentials and roles.'

    def handle(self, *args, **kwargs):
        users = [
            {
                'username': 'ashish',
                'email': 'acharyaaashis906h@gmail.com',
                'password': '*#@12345Acharya',
                'role': 'admin',
            },
            {
                'username': 'lenovo',
                'email': 'acharyaaashish906@gmail.com',
                'password': '*#@123Acharya',
                'role': 'teacher',
            },
            {
                'username': 'ishan',
                'email': 'ishankaphle@gmail.com',
                'password': '220146@ishan',
                'role': 'student',
            },
        ]
        for u in users:
            user, created = User.objects.get_or_create(username=u['username'], defaults={'email': u['email']})
            user.email = u['email']
            user.set_password(u['password'])
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'role': u['role']})
            profile.role = u['role']
            profile.save()
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} user: {u['username']} ({u['role']})"))