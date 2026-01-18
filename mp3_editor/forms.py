from django import forms
from .models import MP3File

class MP3FileForm(forms.ModelForm):
    class Meta:
        model = MP3File
        fields = ('url',)

class MP3UploadForm(forms.ModelForm):
    class Meta:
        model = MP3File
        fields = ['url', 'title', 'artist', 'album', 'genre']
