# Generated by Django 5.1.2 on 2024-11-27 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rp', '0010_comment_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/%Y/%m/%d/', verbose_name='Видео'),
        ),
    ]