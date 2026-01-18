from django.contrib import admin
from django.urls import reverse
from .models import MP3File
import requests
import eyed3
import re
from django.core.files.base import ContentFile
from django.conf import settings
import os

class MP3FileAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'artist', 'album', 'genre')
    readonly_fields = ('download_link', 'embedded_code') # These are still readonly

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Download MP3 file from URL
        response = requests.get(obj.url)
        if response.status_code == 200:
            # Get the filename from the URL
            filename = re.sub(r'[^a-zA-Z0-9\s]', '', obj.artist + ' - ' + obj.title)
            filename = filename + ' - ' + 'jaraflix.com' + '.mp3'
            filename = filename.replace(' ', '-').lower()
            
            # Save MP3 file to model
            obj.file.save(filename, ContentFile(response.content))
            
            # Edit MP3 tags
            audio_file = eyed3.load(obj.file.path)
            
            if audio_file is None:
                print(f"Warning: eyed3 could not load audio file at {obj.file.path}. Tags not applied.")
                return

            if audio_file.tag is None:
                audio_file.initTag()
            
            audio_file.tag.title = obj.title + " | jaraflix.com"
            audio_file.tag.artist = obj.artist
            audio_file.tag.album = obj.album
            audio_file.tag.genre = obj.genre

            # Construct the absolute path to the predefined artwork
            predefined_artwork_path = os.path.join(settings.MEDIA_ROOT, 'images', 'art.jpg')

            if os.path.exists(predefined_artwork_path):
                try:
                    with open(predefined_artwork_path, 'rb') as f:
                        artwork_data = f.read()
                        audio_file.tag.images.set(3, artwork_data, 'image/jpeg')
                except Exception as e:
                    print(f"Error setting artwork for {obj.title}: {e}")
            else:
                print(f"Warning: Artwork file not found at {predefined_artwork_path} for {obj.title}.")

            try:
                audio_file.tag.save()
            except Exception as e:
                print(f"Error saving ID3 tags for {obj.title}: {e}")

            try:
                obj.save() # Crucially, obj.pk will be set AFTER this save for new objects
            except Exception as e:
                print(f"Error saving MP3File object {obj.title}: {e}")
        else:
            print(f"Error: Failed to download MP3 file from URL: {obj.url} (Status Code: {response.status_code})")

    # --- MODIFIED download_link METHOD TO CHECK FOR PK ---
    def download_link(self, obj):
        if obj.pk:          
            download_url = reverse('mp3_editor:download_mp3', args=[obj.pk]) 
            return f'<a href="{download_url}">Download</a>'
        return "(Save to get download link)" # Display a message for new objects

    # --- MODIFIED embedded_code METHOD TO CHECK FOR PK ---
    def embedded_code(self, obj):
        if obj.pk: # Only generate the code if the object has been saved and has a primary key
            return f'<audio controls><source src="{obj.file.url}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
        return "(Save to get embedded code)" # Display a message for new objects

    download_link.short_description = 'Download Link'
    download_link.allow_tags = True
    embedded_code.short_description = 'Embedded Code'
    embedded_code.allow_tags = True

admin.site.register(MP3File, MP3FileAdmin)