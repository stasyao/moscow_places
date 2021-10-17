from django.urls import path

from . import views


urlpatterns = [
    path('', views.show_main_page, name='main_page'),
    path('places/<slug:slug>', views.get_place_details, name='place'),
]
