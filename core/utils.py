import os
import socket
import hashlib
import shutil

from django.urls import reverse


def get_computer_name():
    return socket.gethostname()


def get_file_size(file_path):
    return os.stat(file_path).st_size


def get_file_hash(file_path):
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            _data = f.read(104857600)   # 100k
            if not _data:
                break
            m.update(_data)
    return m.hexdigest()


def copy_file(_from, _to):
    if not os.path.exists(_from):
        raise ValueError('"%s" not exist' % _from)

    if os.path.exists(_to) and not os.path.isdir(_to):
        if get_file_size(_to) == get_file_size(_from):
            if get_file_hash(_to) == get_file_hash(_from):
                return _to

    return shutil.copy2(_from, _to)


def create_file_tag(file_obj, link=True, name=False, height=57):
    file_url = '{url}?p={dir}/{file_name}'.format(
        url=reverse('static_serve'),
        dir=file_obj.file_dir,
        file_name=file_obj.file_name,
    )

    if file_obj.file_type == 'Image':
        tag = '<img src="{url}" style="height:{height}px" />'.format(url=file_url, height=height)
    elif file_obj.file_type == 'Video':
        tag = '<video src="{url}" height="{height}" poster></video>'.format(url=file_url, height=height)
    else:
        tag = '<span style="font-size:23px">{}</span>'.format(file_obj.file_type)

    if name:
        tag += '<br><span style="font-size:9px">{}</span>'.format(file_obj.file_name[-20:])

    if link:
        tag = '<a href="{url}" target="_blank" style="display:block;float:left;margin:2px">{tag}</a>'.format(
            url=file_url, tag=tag)
    return tag
