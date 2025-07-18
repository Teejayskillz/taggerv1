from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mp3/', include('mp3_editor.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)