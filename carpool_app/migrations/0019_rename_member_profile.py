# Generated by Django 4.0.6 on 2022-07-14 01:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carpool_app', '0018_alter_member_contact_number'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Member',
            new_name='Profile',
        ),
    ]