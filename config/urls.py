from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .settings import MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('', include('places.urls')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
