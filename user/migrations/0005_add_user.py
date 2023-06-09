from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def add_user(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    User.objects.create(
        username="UserMigrate",
        email="migrated@admin.com",
        password=make_password("migratedpassword"),
        first_name="Migrated",
        last_name="Improved User",
        is_superuser=True,
        is_staff=True,
    )


def remove_user(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    User.objects.get(email="migrated@admin.com").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_alter_profile_image"),
        ("user", "0002_alter_user_managers_alter_user_email"),
        ("user", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(add_user, remove_user),
    ]
