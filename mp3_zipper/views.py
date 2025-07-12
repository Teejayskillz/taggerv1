# mp3_zipper/views.py
from django.http import HttpResponse
import requests
import zipfile
from io import BytesIO
from .models import MP3Zip

def serve_zip(request, pk):
    mp3_zip = MP3Zip.objects.get(pk=pk)
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        urls = mp3_zip.urls.splitlines()
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                zip_file.writestr(url.split('/')[-1], response.content)
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{mp3_zip.zip_name}.zip"'
    return response

def download_zip(request, pk):
    mp3_zip = MP3Zip.objects.get(pk=pk)
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        urls = mp3_zip.urls.splitlines()
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                zip_file.writestr(url.split('/')[-1], response.content)
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{mp3_zip.zip_name}.zip"'
    return response