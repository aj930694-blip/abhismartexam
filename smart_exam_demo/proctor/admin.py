from django.contrib import admin
from django.apps.registry import AppRegistryNotReady
from django.core.exceptions import ImproperlyConfigured

try:
    from proctor.models import Violation
except (ImproperlyConfigured, AppRegistryNotReady):
    Violation = None

if Violation is not None:
    admin.site.register(Violation)