from django.db import models

class MP3File(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True, null=True)
    artist = models.CharField(max_length=255, blank=True, null=True)
    album = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='mp3_files/', blank=True, null=True)
    artwork = models.ImageField(upload_to='artwork/', blank=True, null=True)