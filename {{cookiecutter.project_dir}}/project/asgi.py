import readenv.loads  # noqa: F401 isort:skip
import django_service_urls.loads  # noqa: F401 isort:skip

readenv.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_name }}.settings.local")

from django.core.asgi import get_asgi_application  # noqa: E402

application = get_asgi_application()
