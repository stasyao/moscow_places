from django.contrib import admin
from .models import Image, Place


class PlacesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Place, PlacesAdmin)

class ImagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image)
