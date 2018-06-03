import os

from django.core.management import BaseCommand, CommandError

from core import models
from core.utils import get_computer_name, get_file_size, get_file_hash


class Command(BaseCommand):
    help = 'scan a dir'

    def add_arguments(self, parser):
        parser.add_argument('dir')

    def handle(self, **options):
        if not os.path.exists(options['dir']):
            raise CommandError('dir not exists')

        # models.File.objects.all().delete()

        file_exts = [i.lower() for i in models.FileExt.objects.all().values_list('file_ext', flat=True)]

        computer_name = get_computer_name()
        for dir_name, sub_dirs, files in os.walk(options['dir']):
            for file_name in files:
                dir_name = os.path.abspath(dir_name)
                if os.sep == '\\':
                    dir_name = dir_name.replace('\\', '/')
                full_path = os.path.join(dir_name, file_name)

                if os.path.splitext(file_name)[-1].lower() not in file_exts:
                    print('***', full_path)
                    continue
                else:
                    print('---', full_path)

                file_size = get_file_size(full_path)
                file_hash = get_file_hash(full_path)
                models.FileScan.add_scan(computer_name, dir_name, file_name, file_size, file_hash)
