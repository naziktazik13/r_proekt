# Generated by Django 5.1.2 on 2024-11-25 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rp', '0002_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image',
            new_name='media',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
