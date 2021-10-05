from django.urls import path

from . import views


urlpatterns = [
    path('', views.show_main_page, name='main_page'),
    path('<int:place_id>', views.get_location_details, name='location'),
]
