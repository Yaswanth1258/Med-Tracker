import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracker_core.settings')
django.setup()

from django.contrib.auth.models import Group

roles = ['Patient', 'Caregiver', 'Doctor']
for role in roles:
    group, created = Group.objects.get_or_create(name=role)
    if created:
        print(f"Created group: {role}")
    else:
        print(f"Group already exists: {role}")
