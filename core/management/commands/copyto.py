import os

from django.core.management import BaseCommand, CommandError

from core import models
from core.utils import copy_file


class Command(BaseCommand):
    help = 'copyto a dir'

    def add_arguments(self, parser):
        parser.add_argument('to_dir')

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

            to_file = os.path.join(to_dir, file.file_name)

            print('--', file.full_path, '->', to_file)

            copy_file(file.full_path, to_file)

            models.FileCopy(
                file_hash_obj=file_hash_obj,
                from_file=file.full_path,
                to_file=to_file,
            ).save()
