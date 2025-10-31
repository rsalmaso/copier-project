#!/usr/bin/env python

import readenv.loads  # noqa: F401 isort:skip
import django_service_urls.loads  # noqa: F401 isort:skip

import sys


def main():
    readenv.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
