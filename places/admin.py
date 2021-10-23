from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from django import forms
from django.contrib import admin
from django.forms import Textarea
from django.utils.html import format_html

from .models import Image, Place



@admin.action(description='Превью')
def picture_preview(obj):
    return format_html(
        '<img src="{}"'
        'style="object-fit: cover; width:200px; height:150px;" />',
        obj.image.url
    )


@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    raw_id_fields = ('place',)
    list_display = ('place', picture_preview, )
    readonly_fields = [picture_preview, ]

    def has_module_permission(self, request):
        """
        Раздел "Изображения" на стартовой странице админ-панели
        скрываем от всех, кто входит в группу "контент-менеджеры"
        """
        if request.user.groups.filter(name='content_managers').exists():
            return False
        return super().has_module_permission(request)


class ImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Image
    fields = ['image', 'priority', picture_preview, ]
    readonly_fields = [picture_preview, ]
    extra = 0


    def get_formset(self, request, obj=None, **kwargs):
        """
        Цель - не допустить перевода в статус "Опубликован"
        (=размещения на карте) записи без, как минимум, одного изображения.
        Проверка работает как в сценарии создания новой записи, так и в
        сценарии изменения существующей (включая попытку изменения статуса с 
        одновременным удалением единственной фотографии).

        Существующие верхнеуровные настройки (через атрибут `min_nums` или 
        переопределение `get_min_nums`) для данной цели не подходят.
        Первая настройка жестко выставляет обязательный инлайн, без возможности 
        динамичной корректировки.
        Вторая настройка также не подходит, т.к. работает только при уже 
        инициированной инлайн-форме (такое инициирование не происходит в 
        сценарии первоначального создания записи, которая по дефолту со 
        статусом "draft").
        """
        formset = super().get_formset(request, obj=obj, **kwargs)
        if request.POST.get('pub_status') == 'P':
            formset.min_num = 1
            formset.validate_min = True 
        return formset


class PlaceAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Place
        fields = '__all__'
        widgets = {
            'description_short': Textarea(attrs={'cols': 80, 'rows': 5})
        }

    def clean(self):
        super().clean()
        if self.data.get('pub_status') == 'P' and not all(
            [
                self.data.get('description_short'),
                self.data.get('description_long'),
                self.data.get('longitude'),
                self.data.get('latitude')
            ]
        ):
            raise forms.ValidationError(
                'Для перевода в статус "Опубликовано" '
                'должны быть заполнены все поля'
            )


@admin.action(description='Опубликовать все отмеченные локации')
def make_published(modeladmin, request, queryset):
    queryset.update(pub_status='P')


@admin.register(Place)
class PlacesAdmin(admin.ModelAdmin, SortableAdminMixin):
    inlines = [ImageInline, ]
    form = PlaceAdminForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'pub_status',)
    ordering = ('title',)
    search_fields = ('title',)
    actions = [make_published]
