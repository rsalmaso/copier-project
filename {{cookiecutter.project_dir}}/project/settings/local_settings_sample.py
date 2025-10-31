# This is a sample custom local settings example
#
# Usage
# Set DJANGO_SETTINGS_MODULE env var:
#   $ DJANGO_SETTINGS_MODULE=local_settings manage.py help
# or via manage.py --settings option:
#   $ manage.py help --settings local_settings
# or via .env file:
#   $ echo "DJANGO_SETTINGS_MODULE=local_settings" >> $PROJECT_ROOT/.env
#   $ manage.py help

import readenv

env = readenv.str("ENV", "local")
match env:
    case "local":
        from {{ cookiecutter.project_dir }}.settings.local import *  # noqa: E402,F401,F403
    case "production":
        from {{ cookiecutter.project_dir }}.settings.production import *  # noqa: E402,F401,F403
    case "staging":
        from {{ cookiecutter.project_dir }}.settings.staging import *  # noqa: E402,F401,F403
    case _:
        raise RuntimeError(f"unknown {env!r} setting")

LOGGING = get_logging_conf(min_log_level="INFO")  # type: ignore[name-defined]  # noqa: F405
