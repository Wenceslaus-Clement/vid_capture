# Generated by Django 4.0 on 2024-09-25 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_video_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='features',
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
