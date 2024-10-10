# base/models.py

from django.db import models

class Video(models.Model):
    """
    Video model to store uploaded videos with metadata, including title, duration, and extracted features.
    """
    title = models.CharField(max_length=255, blank=True, null=True)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(blank=True, null=True)
    features = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else 'Unnamed Video'
