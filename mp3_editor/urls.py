from django.urls import path
from . import views
from .views import upload_mp3, upload_success

app_name = 'mp3_editor'

urlpatterns = [
    path('download/mp3/<int:pk>/', views.download_mp3_file, name='download_mp3'),
    path('upload/', upload_mp3, name='upload_mp3'),
    path('success/<int:pk>/', upload_success, name='upload_success'),

]
