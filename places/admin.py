from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import Textarea
from django.utils.html import format_html

from .models import Image, Place


admin.site.unregister(Group)


@admin.action(description='Превью')
def picture_preview(obj):
    return format_html(
        '<img src="{}"'
        'style="object-fit: cover; width:200px;height:150px;" />',
        obj.image.url
    )


@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('location', picture_preview, )
    readonly_fields = [picture_preview, ]

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            return {}
        return super().get_model_perms(request)


class ImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Image
    fields = ['image', 'priority', picture_preview, ]
    readonly_fields = [picture_preview, ]
    extra = 0


class PlaceAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].disabled = True

    class Meta:
        model = Place
        fields = '__all__'
        widgets = {
            'title': Textarea(attrs={'cols': 80, 'rows': 5}),
            'description_short': Textarea(attrs={'cols': 80, 'rows': 5}),
            'slug': forms.HiddenInput()
        }


@admin.register(Place)
class PlacesAdmin(admin.ModelAdmin, SortableAdminMixin):
    inlines = [ImageInline, ]
    form = PlaceAdminForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)
    ordering = ('title',)
    search_fields = ('title',)
