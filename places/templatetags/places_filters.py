import json

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(is_safe=True)
def json_script_with_non_ascii(value, element_id):
    from django.core.serializers.json import DjangoJSONEncoder
    _json_script_escapes = {
        ord('>'): '\\u003E',
        ord('<'): '\\u003C',
        ord('&'): '\\u0026',
    }
    json_str = json.dumps(
        value, cls=DjangoJSONEncoder, ensure_ascii=False).translate(_json_script_escapes)
    return format_html(
        '<script id="{}" type="application/json">{}</script>',
        element_id, mark_safe(json_str)
    )
