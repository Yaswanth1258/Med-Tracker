import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracker_core.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")

if not username or not password:
    print("Admin credentials are not configured.")
else:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email or "",
            "is_staff": True,
            "is_superuser": True,
        }
    )

    if created:
        user.set_password(password)
        user.save()
        print(f"Admin user '{username}' created successfully.")
    else:
        print(f"Admin user '{username}' already exists.")

        if not user.is_staff or not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("Existing user promoted to admin.")
