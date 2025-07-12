# mp3_zipper/admin.py
from django.contrib import admin
from django.core.files.base import ContentFile
from .models import MP3Zip
import requests
import zipfile
from io import BytesIO

class MP3ZipAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            urls = obj.urls.splitlines()
            for url in urls:
                response = requests.get(url)
                if response.status_code == 200:
                    zip_file.writestr(url.split('/')[-1], response.content)
        zip_buffer.seek(0)
        obj.zip_file.save(f'{obj.zip_name}.zip', ContentFile(zip_buffer.read()))
        obj.save()

admin.site.register(MP3Zip, MP3ZipAdmin)