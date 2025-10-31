import readenv.loads  # noqa: F401 isort:skip
import django_service_urls.loads  # noqa: F401 isort:skip

readenv.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_name }}.settings.local")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
