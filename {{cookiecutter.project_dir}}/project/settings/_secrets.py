"""
This file initialize all sensitive config values
which must not be shared with outside world
ie: tokens, passwords, hash keys, ecc

every config key exported from this file will populate the
custom exception filter to hide them in the debug email/template
"""

import getpass
import os
import readenv

SECRET_KEY = readenv.str("SECRET_KEY")
SENTRY_DSN = readenv.str("SENTRY_DSN", "")

DATABASES = {
    "default": readenv.get(
        "DATABASE_URL",{% if cookiecutter.use_postgresql == "y" %}
        "postgresql://{user}:{password}@db:5432/{{ cookiecutter.db_name }}",{% else %}
        f"sqlite:///app/{rel('{{ cookiecutter.db_name }}.db')}",{% endif %}
    ),
}


EMAIL_BACKEND = readenv.str("EMAIL_BACKEND", "console://")


# keep always HIDDEN_SETTINGS and __all__ as last items (DATABASE_* are not exported as setting values)
# HIDDEN_SETTINGS is used by janine.views.debug.ExceptionReporterFilter
hidden_settings = [key for key in locals().keys() if key.isupper()]
HIDDEN_SETTINGS = hidden_settings + [f"DATABASE_{key}" for key in ["NAME", "USER", "PASSWORD", "HOST", "PORT"]]

__all__ = hidden_settings + ["HIDDEN_SETTINGS"]
