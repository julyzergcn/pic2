import os

from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property


class File(models.Model):
    computer_name = models.CharField(max_length=100)
    file_dir = models.TextField()
    file_name = models.CharField(max_length=255)

    file_exist = models.BooleanField(default=True)
    file_size = models.PositiveIntegerField()

    file_hash_obj = models.ForeignKey('FileHash', on_delete=models.CASCADE,
                                      related_name='files', null=True, blank=True)

    @cached_property
    def full_path(self):
        return os.path.abspath(os.path.join(self.file_dir, self.file_name))

    def __str__(self):
        return '{} - {}'.format(self.computer_name, self.full_path)

    @property
    def file_type(self):
        ext = os.path.splitext(self.file_name)[-1]
        return FileExt.get_file_type(ext)


class FileScan(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='scans')
    scan_date = models.DateTimeField(default=timezone.now)

    file_exist = models.BooleanField()
    file_size = models.PositiveIntegerField(default=0)
    file_hash = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return '{}'.format(self.pk)


class FileHash(models.Model):
    file_hash = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return '{}'.format(self.file_hash)


class FileCopy(models.Model):
    file_hash_obj = models.ForeignKey(FileHash, on_delete=models.CASCADE, related_name='copies')
    copy_date = models.DateTimeField(default=timezone.now)

    from_file = models.TextField()
    to_file = models.TextField()

    def __str__(self):
        return '{}'.format(self.pk)

    class Meta:
        verbose_name_plural = 'File Copies'


class FileExt(models.Model):
    FILE_TYPES = (
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('Audio', 'Audio'),
    )

    file_ext = models.CharField(max_length=20)
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)

    def __str__(self):
        return '{}'.format(self.file_ext)

    @classmethod
    def get_file_type(cls, ext):
        try:
            obj = cls.objects.filter(file_ext__iexact=ext.lower())[0]
        except IndexError:
            return 'Unknown'
        else:
            return obj.file_type
