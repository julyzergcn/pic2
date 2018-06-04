from django import template
from django.utils.safestring import mark_safe

from core.models import File, FileHash
from core.utils import create_file_tag as _create_file_tag

register = template.Library()


@register.simple_tag
def create_file_tag(obj):
    if isinstance(obj, File):
        return mark_safe(_create_file_tag(obj, link=True, name=True))
    elif isinstance(obj, FileHash):
        html = '<div style="border:1px solid #ccc;float:left;margin:4px 5px">'
        for _file in obj.files.all():
            html += _create_file_tag(_file, link=True, name=True)
        html += '<div style="clear:both"></div></div>'
        return mark_safe(html)
    return ''
