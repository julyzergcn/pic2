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

    @classmethod
    def add_scan(cls, computer_name, file_dir, file_name, file_size, file_hash, file_exist=True):
        file_hash_obj,c = FileHash.objects.get_or_create(file_hash=file_hash)

        kwargs = dict(computer_name=computer_name,
                      file_dir=file_dir,
                      file_name=file_name)

        try:
            file = File.objects.filter(**kwargs)[0]
        except IndexError:
            file = File(**kwargs)

        file.file_exist = file_exist
        file.file_size = file_size
        file.file_hash_obj = file_hash_obj
        file.save()

        file_scan = FileScan(file=file)
        file_scan.file_exist = file_exist
        file_scan.file_size = file_size
        file_scan.file_hash = file_hash
        file_scan.save()

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
