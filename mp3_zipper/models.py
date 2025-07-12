# mp3_zipper/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import zipfile
from io import BytesIO
from django.http import HttpResponse

class MP3Zip(models.Model):
    zip_name = models.CharField(max_length=255)
    urls = models.TextField()
    zip_file = models.FileField(upload_to='zip_files/', blank=True, null=True)


@receiver(post_save, sender=MP3Zip)
def zip_mp3_files(sender, instance, **kwargs):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        urls = instance.urls.splitlines()
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                zip_file.writestr(url.split('/')[-1], response.content)
    zip_buffer.seek(0)
    # Save the zip file to a file field or serve it as a response
    # For now, let's just print the zip buffer
    print(zip_buffer.read())