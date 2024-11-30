# Generated by Django 5.1.2 on 2024-11-27 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rp', '0007_remove_comment_active_comment_dislikes_comment_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='rp.comment', verbose_name='Родительский комментарий'),
        ),
    ]