# your_app_name/views.py (create this file if it doesn't exist)
import os
import re
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from wsgiref.util import FileWrapper # Efficiently serves large files
from django.shortcuts import render, redirect
from .forms import MP3UploadForm
from .utils import process_mp3


# Assuming your MP3File model is in your_app_name/models.py
from .models import MP3File 

def download_mp3_file(request, pk):
    # Get the MP3File object based on its primary key (pk)
    mp3_file_obj = get_object_or_404(MP3File, pk=pk)
    
    # Get the absolute path to the stored MP3 file
    file_path = mp3_file_obj.file.path
    
    # Check if the file actually exists on the filesystem
    if os.path.exists(file_path):
        # Use FileWrapper for efficient serving of large files
        wrapper = FileWrapper(open(file_path, 'rb'))
        
        # Generate a clean filename for the download that will appear to the user
        # This uses the same logic you had for saving the file, but now for download name
        download_filename = f"{mp3_file_obj.artist} - {mp3_file_obj.title} - jaraflix.com.mp3"
        # Clean the filename to be safe for various operating systems and browsers
        download_filename = re.sub(r'[^\w\s\.\-]', '', download_filename).strip()
        download_filename = re.sub(r'\s+', ' ', download_filename).replace(' ', '_').lower()

        # Create an HttpResponse object with the file content
        response = HttpResponse(wrapper, content_type='audio/mpeg')
        
        # Set the Content-Length header for proper download progress indication
        response['Content-Length'] = os.path.getsize(file_path)
        
        # THIS IS THE CRUCIAL HEADER: Forces the browser to download the file
        # 'attachment' forces download, 'filename' provides the suggested file name
        response['Content-Disposition'] = f'attachment; filename="{download_filename}"'
        
        return response
    else:
        # If the file doesn't exist on disk, return a 404 error
        return HttpResponse("File not found.", status=404)
    

def upload_mp3(request):
    if request.method == 'POST':
        form = MP3UploadForm(request.POST)
        if form.is_valid():
            mp3 = form.save(commit=False)
            mp3.save()
            process_mp3(mp3)

            return redirect('mp3_editor:upload_success', pk=mp3.pk)
    else:
        form = MP3UploadForm()

    return render(request, 'mp3_editor/upload.html', {'form': form})


def upload_success(request, pk):
    from .models import MP3File
    mp3 = MP3File.objects.get(pk=pk)
    return render(request, 'mp3_editor/success.html', {'mp3': mp3})
