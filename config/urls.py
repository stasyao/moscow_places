from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views
from .settings import MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('', views.show_start_page),
    path('admin/', admin.site.urls),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
