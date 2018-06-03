import mimetypes
import os
import posixpath
import stat

from django.http import FileResponse, Http404, HttpResponseNotModified
from django.utils._os import safe_join
from django.utils.http import http_date
from django.views.static import was_modified_since


def static_serve(request):
    path = request.GET.get('p') or ''
    file_path = posixpath.normpath(path)

    if not os.path.exists(file_path):
        raise Http404('"%s" does not exist' % file_path)
    if os.path.isdir(file_path):
        raise Http404('"%s" is dir' % file_path)

    statobj = os.stat(file_path)
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified()

    content_type, encoding = mimetypes.guess_type(file_path)
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response["Last-Modified"] = http_date(statobj.st_mtime)

    if stat.S_ISREG(statobj.st_mode):
        response["Content-Length"] = statobj.st_size
    if encoding:
        response["Content-Encoding"] = encoding
    return response
