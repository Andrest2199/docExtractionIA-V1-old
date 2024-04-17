"""
WSGI config for grupo_ono_ocr project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application 
from django.conf import settings
import sys

# Append the parent directory of 'src' to sys.path
sys.path.append('/opt/bitnami/projects/grupo-ono-ocr')

os.environ["DJANGO_SETTINGS_MODULE"] = "src.settings"
if not settings.DEBUG:
    os.environ["PYTHON_EGG_CACHE"] = (
        "/opt/bitnami/projects/grupo-ono-ocr/egg_cache"
    )

application = get_wsgi_application()
