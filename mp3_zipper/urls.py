# mp3_zipper/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('serve_zip/<pk>/', views.serve_zip, name='serve_zip'),
    path('download_zip/<pk>/', views.download_zip, name='download_zip'),
]