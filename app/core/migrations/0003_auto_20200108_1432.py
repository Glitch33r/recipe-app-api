# Generated by Django 3.0.1 on 2020-01-08 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='yser',
            new_name='user',
        ),
    ]
