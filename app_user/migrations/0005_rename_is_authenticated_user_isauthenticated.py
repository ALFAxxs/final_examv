# Generated by Django 5.0.6 on 2024-06-10 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0004_user_is_authenticated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_authenticated',
            new_name='isauthenticated',
        ),
    ]