from django.contrib import admin
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.db.models import Count

from core import models
from core.utils import create_file_tag


class FileScanInline(admin.TabularInline):
    model = models.FileScan
    extra = 0
    readonly_fields = ('scan_date', 'file_exist', 'file_size', 'file_hash')


class NewChangeListMixin:
    def get_changelist(self, request, **kwargs):
        ChangeList = super().get_changelist(request, **kwargs)
        class NewChangeList(ChangeList):
            def get_filters_params(self2, params=None):
                new_params = super().get_filters_params(params)
                if 'layout' in new_params:
                    del new_params['layout']
                return new_params
        return NewChangeList

    def changelist_view(self, request, extra_context=None):
        if request.GET.get('layout') == 'default':
            return redirect(request.path)
        response = super().changelist_view(request, extra_context)
        if request.GET.get('layout') == 'new':
            response.template_name = 'admin/core/change_list_new_layout.html'
        return response


@admin.register(models.File)
class FileAdmin(NewChangeListMixin, admin.ModelAdmin):
    list_display = ('file_tag', 'file_name', 'file_dir', 'computer_name', 'file_exist', 'file_size')
    list_display_links = ('file_name',)
    list_filter = ('file_exist', 'computer_name')
    search_fields = ('file_dir', 'file_name')
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


class HasFilesFilter(admin.SimpleListFilter):
    title = 'Has Files'
    parameter_name = 'has_files'

    def lookups(self, request, model_admin):
        return (
            ('more_than_one', '>1'),
            ('only_one', '=1'),
            ('at_least_one', '>=1'),
            ('zero', '=0'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'more_than_one':
            return queryset.annotate(files_count=Count('files')).filter(files_count__gt=1)
        elif self.value() == 'only_one':
            return queryset.annotate(files_count=Count('files')).filter(files_count=1)
        elif self.value() == 'at_least_one':
            return queryset.annotate(files_count=Count('files')).filter(files_count__gte=1)
        elif self.value() == 'zero':
            return queryset.annotate(files_count=Count('files')).filter(files_count=0)
        return queryset


@admin.register(models.FileHash)
class FileHashAdmin(NewChangeListMixin, admin.ModelAdmin):
    list_display = ('file_tags', 'file_hash')
    list_display_links = ('file_hash',)
    list_filter = (HasFilesFilter,)
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
