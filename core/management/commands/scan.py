import os

from django.core.management import BaseCommand, CommandError

from core import models
from core.utils import get_computer_name, get_file_size, get_file_hash


class Command(BaseCommand):
    help = 'scan a dir'

    def add_arguments(self, parser):
        parser.add_argument('dir')
        parser.add_argument('--new', action='store_true', dest='new_scan')

    def handle(self, **options):
        if not os.path.exists(options['dir']):
            raise CommandError('dir not exists')

        # models.File.objects.all().delete()

        file_exts = [i.lower() for i in models.FileExt.objects.all().values_list('file_ext', flat=True)]

        num = 1
        computer_name = get_computer_name()
        for dir_name, sub_dirs, files in os.walk(options['dir']):
            for file_name in files:
                dir_name = os.path.abspath(dir_name)
                if os.sep == '\\':
                    dir_name = dir_name.replace('\\', '/')
                full_path = os.path.join(dir_name, file_name)

                if os.path.splitext(file_name)[-1].lower() not in file_exts:
                    # print('**', full_path)
                    print(num)
                    num += 1
                    continue
                else:
                    print('--', full_path)

                kwargs = dict(computer_name=computer_name,
                              file_dir=dir_name,
                              file_name=file_name)

                file_obj_exist = False
                try:
                    file = models.File.objects.filter(**kwargs)[0]
                except IndexError:
                    file = models.File(**kwargs)
                else:
                    file_obj_exist = True

                if file_obj_exist and not options['new_scan']:
                    print('** skip')
                    continue

                file_hash = get_file_hash(full_path)

                file_hash_obj,c = models.FileHash.objects.get_or_create(file_hash=file_hash)

                file_size = get_file_size(full_path)

                if not file_obj_exist:
                    file.file_exist = True
                    file.file_size = file_size
                    file.file_hash_obj = file_hash_obj
                    file.save()

                if options['new_scan']:
                    if file_obj_exist:
                        uf = []
                        if file.file_exist != True:
                            file.file_exist = True
                            uf.append('file_exist')
                        if file.file_size != file_size:
                            file.file_size = file_size
                            uf.append('file_size')
                        if file.file_hash_obj != file_hash_obj:
                            file.file_hash_obj = file_hash_obj
                            uf.append('file_hash_obj')
                        if uf:
                            file.save(update_fields=uf)

                    file_scan = models.FileScan(file=file)
                    file_scan.file_exist = True
                    file_scan.file_size = file_size
                    file_scan.file_hash = file_hash
                    file_scan.save()
