# Generated by Django 4.2.5 on 2024-04-18 05:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_remove_order_address_remove_order_fullname_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Address',
            new_name='UserAddress',
        ),
    ]
