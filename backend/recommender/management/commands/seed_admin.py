from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recommender.models import UserProfile

class Command(BaseCommand):
    help = 'Create default admin user (admin / admin123)'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username='admin')
        user.set_password('admin123')
        user.is_staff = True
        user.is_superuser = True
        user.first_name = 'Admin'
        user.email = 'admin@idpdr.ai'
        user.save()
        UserProfile.objects.update_or_create(user=user, defaults={'role': 'admin'})
        status = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{status} admin user: admin / admin123'))
