"""
Constance configuration file for project
Put here only constance related settings.
"""

import datetime as dt

from django.core.validators import RegexValidator

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_SUPERUSER_ONLY = False
CONSTANCE_ADDITIONAL_FIELDS = {}

CONSTANCE_CONFIG_FIELDSETS = {}

CONSTANCE_CONFIG = {}


__all__ = [key for key in locals().keys() if key.isupper()]  # keep always as last item
