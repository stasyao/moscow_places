from django import forms
from django.contrib import admin
from django.forms import Textarea
from django.utils.safestring import mark_safe

from .models import Image, Place


def picture_preview(obj):
    return mark_safe(
        f'<img src="{obj.image.url}"'
        f'style="object-fit: cover; width:200px;height:150px;" />'
    )


@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('location', picture_preview, )
    readonly_fields = [ picture_preview ]


class ImageInline(admin.TabularInline):
    model = Image
    fields = [ 'image', 'priority', picture_preview ]
    readonly_fields = [ picture_preview ]
    extra = 0


class PlaceAdminForm(forms.ModelForm):
    longitude = forms.CharField(max_length=50)
    latitude = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']
        kwargs['initial'] = {
            'longitude': instance.coordinates['lng'],
            'latitude': instance.coordinates['lat']
        }
        super().__init__(*args, **kwargs)

    class Meta:
        model = Place
        exclude = ['coordinates']
        widgets = {
            'title': Textarea(attrs={'cols': 80, 'rows': 5}),
            'description_short': Textarea(attrs={'cols': 80, 'rows': 5})
        }


@admin.register(Place)
class PlacesAdmin(admin.ModelAdmin):
    inlines = [ ImageInline, ]
    form = PlaceAdminForm

    def save_model(self, request, obj, form, change):
        obj.coordinates = {
            'lng': form.cleaned_data['longitude'],
            'lat': form.cleaned_data['latitude']
        }
        super().save_model(request, obj, form, change)
