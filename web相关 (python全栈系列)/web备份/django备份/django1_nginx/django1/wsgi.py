"""
WSGI config for django1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#add
from os.path import join,dirname,abspath
PROJECT_DIR = dirname(dirname(abspath(__file__)))
import sys
sys.path.insert(0,PROJECT_DIR)
sys.path.append('/var/www/files')
#add end


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django1.settings')

application = get_wsgi_application()
