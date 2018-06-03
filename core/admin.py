from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from core import models


def create_file_tag(file_obj, link=True, name=False):
    file_url = '{url}?p={dir}/{file_name}'.format(
        url=reverse('static_serve'),
        dir=file_obj.file_dir,
        file_name=file_obj.file_name,
    )

    if file_obj.file_type == 'Image':
        tag = '<img src="{url}" style="height:{height}px" />'.format(url=file_url, height=53)
    elif file_obj.file_type == 'Video':
        tag = '<video src="{url}" height="{height}" poster></video>'.format(url=file_url, height=53)
    else:
        tag = '<span style="font-size:23px">{}</span>'.format(file_obj.file_type)

    if name:
        tag += '<br><span style="font-size:9px">{}</span>'.format(file_obj.file_name[-20:])

    if link:
        tag = '<a href="{url}" target="_blank" style="display:block;float:left;margin-left:2px">{tag}</a>'.format(url=file_url, tag=tag)
    return tag


class FileScanInline(admin.TabularInline):
    model = models.FileScan
    extra = 0
    readonly_fields = ('scan_date', 'file_exist', 'file_size', 'file_hash')


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_tag', 'file_name', 'file_dir', 'computer_name', 'file_exist', 'file_size')
    list_display_links = ('file_name',)
    list_filter = ('file_exist', 'computer_name')
    inlines = (FileScanInline,)

    def file_tag(self, obj):
        return mark_safe(create_file_tag(obj))


@admin.register(models.FileScan)
class FileScanAdmin(admin.ModelAdmin):
    list_display = ('file', 'file_exist', 'file_size', 'file_hash', 'scan_date')


class FileCopyInline(admin.TabularInline):
    model = models.FileCopy
    extra = 0
    readonly_fields = ('copy_date', 'from_file', 'to_file')


@admin.register(models.FileHash)
class FileHashAdmin(admin.ModelAdmin):
    list_display = ('file_tags', 'file_hash')
    list_display_links = ('file_hash',)
    search_fields = ('file_hash',)
    inlines = (FileCopyInline,)

    def file_tags(self, obj):
        lst = [create_file_tag(f, name=True) for f in obj.files.all()]
        return mark_safe(''.join(lst))


@admin.register(models.FileCopy)
class FileCopyAdmin(admin.ModelAdmin):
    list_display = ('file_hash_obj', 'copy_date', 'from_file', 'to_file')
    search_fields = ('file_hash_obj__file_hash', 'from_file')


@admin.register(models.FileExt)
class FileExtAdmin(admin.ModelAdmin):
    list_display = ('file_ext', 'file_type')
    list_filter = ('file_type',)
