from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.show_start_page),
    path('admin/', admin.site.urls),
]
