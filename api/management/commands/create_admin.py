# from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model
# import os

# class Command(BaseCommand):
#     help = 'Create default admin user'

#     def handle(self, *args, **kwargs):
#         User = get_user_model()
#         username = os.getenv("DJANGO_ADMIN_USER")
#         email = os.getenv("DJANGO_ADMIN_EMAIL")
#         password = os.getenv("DJANGO_ADMIN_PASS")

#         if not User.objects.filter(username=username).exists():
#             User.objects.create_superuser(username=username, email=email, password=password)
#             self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
#         else:
#             self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists."))
