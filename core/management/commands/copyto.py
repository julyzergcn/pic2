import os

from django.core.management import BaseCommand, CommandError

from core import models
from core.utils import copy_file, get_file_size, get_file_hash


class Command(BaseCommand):
    help = 'copyto a dir'

    def add_arguments(self, parser):
        parser.add_argument('to_dir')
        parser.add_argument('--new', action='store_true', dest='new_copy')

    def handle(self, **options):
        to_dir = os.path.abspath(options['to_dir'])

        if not os.path.exists(to_dir):
            os.makedirs(to_dir, exist_ok=True)
        if not os.path.exists(to_dir):
            raise CommandError('"%s" not exists' % to_dir)

        for file_hash_obj in models.FileHash.objects.all():
            try:
                file = file_hash_obj.files.all()[0]
            except IndexError:
                continue

            to_file_dir = os.path.join(to_dir, *file.file_dir.split('/')[1:])

            if not os.path.exists(to_file_dir):
                os.makedirs(to_file_dir, exist_ok=True)

            to_file = os.path.join(to_file_dir, file.file_name)

            if os.path.exists(to_file):
                if get_file_size(to_file) == file.file_size:
                    if get_file_hash(to_file) == file.file_hash_obj.file_hash:
                        print('** skip', file.full_path)
                        continue

            print('--', file.full_path, '->', to_file)

            copy_file(file.full_path, to_file)

            if options['new_copy']:
                models.FileCopy(
                    file_hash_obj=file_hash_obj,
                    from_file=file.full_path,
                    to_file=to_file,
                ).save()
