# Generated by Django 4.0 on 2024-09-25 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_video_video_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='features',
        ),
    ]
