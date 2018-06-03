import os
import socket
import hashlib
import shutil


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
