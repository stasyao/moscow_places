from django.contrib import admin
from .models import Place


class PlacesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Place, PlacesAdmin)
