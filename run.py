#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
from gevent.wsgi import WSGIServer

import sys
import os
import traceback

from django.core.signals import got_request_exception
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simplechat.settings")
port = len(sys.argv) > 1 and int(sys.argv[1]) or 8000


def exception_printer(sender, **kwargs):
    traceback.print_exc()


got_request_exception.connect(exception_printer)


from django.core.handlers.wsgi import WSGIHandler
WSGIServer(('', port), WSGIHandler()).serve_forever()
