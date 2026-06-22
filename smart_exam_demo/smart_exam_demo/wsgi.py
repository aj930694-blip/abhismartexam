import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'smart_exam_demo.settings'
)

application = get_wsgi_application()