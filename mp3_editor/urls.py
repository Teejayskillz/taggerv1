from django.urls import path
from . import views

app_name = 'mp3_editor'

urlpatterns = [
    path('download/mp3/<int:pk>/', views.download_mp3_file, name='download_mp3'),
]