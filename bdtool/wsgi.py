"""
WSGI config for bdtool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/ongraph/code/bdtool/bdtool')

os.environ["DJANGO_SETTINGS_MODULE"] = "bdtool.settings"
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bdtool.settings")

application = get_wsgi_application()
