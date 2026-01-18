import requests
import eyed3
import os
import re
from django.conf import settings
from django.core.files.base import ContentFile

def process_mp3(obj):
    response = requests.get(obj.url)

    if response.status_code != 200:
        raise Exception("Failed to download MP3")

    filename = re.sub(r'[^a-zA-Z0-9\s]', '', f"{obj.artist} - {obj.title}")
    filename = filename.replace(' ', '-').lower()
    filename = f"{filename}-jaraflix.com.mp3"

    obj.file.save(filename, ContentFile(response.content))

    audio_file = eyed3.load(obj.file.path)
    if audio_file is None:
        return

    if audio_file.tag is None:
        audio_file.initTag()

    audio_file.tag.title = f"{obj.title} | jaraflix.com"
    audio_file.tag.artist = obj.artist
    audio_file.tag.album = obj.album
    audio_file.tag.genre = obj.genre

    artwork_path = os.path.join(settings.MEDIA_ROOT, 'images', 'art.jpg')
    if os.path.exists(artwork_path):
        with open(artwork_path, 'rb') as f:
            audio_file.tag.images.set(3, f.read(), 'image/jpeg')

    audio_file.tag.save()
    obj.save()
