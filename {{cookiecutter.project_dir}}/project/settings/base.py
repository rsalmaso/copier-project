"""
Django settings for {{ cookiecutter.project_name }} project.
"""

import readenv.loads  # noqa: F401 isort:skip

from ._cache import *  # noqa: F401,F403{% if cookiecutter.project_type == "django-cms" %}
from ._cms import *  # noqa: F401,F403{% endif %}{% if cookiecutter.use_djangorestframework == "y" %}
from ._drf import *  # noqa: F401,F403{% endif %}
from ._email import *  # noqa: F401,F403
from ._logging import *  # noqa: F401,F403
from ._paths import *  # noqa: F401,F403
from ._paths import var_rel
from ._secrets import *  # noqa: F401,F403

ENV = readenv.str("ENV", "")


PROJECT_NAME = "{{ cookiecutter.project_name }}"

DEBUG = readenv.bool("DEBUG", "false")
DEFAULT_EXCEPTION_REPORTER_FILTER = readenv.str(
    "DEFAULT_EXCEPTION_REPORTER_FILTER", "project.debug.ExceptionReporterFilter"
)
# LANGUAGES = [
#     ("it", _("Italian")),
#     ("en", _("English")),
# ]

ADMINS = [
    # "Your Name <your_email@example.com>",
]

MANAGERS = ADMINS

ALLOWED_HOSTS = readenv.list("ALLOWED_HOSTS", [""])

# CSRF protection for HTTPS requests through reverse proxy
CSRF_TRUSTED_ORIGINS = readenv.list("CSRF_TRUSTED_ORIGINS", [])

TIME_ZONE = readenv.str("TIME_ZONE", "Europe/Rome")
LANGUAGE_CODE = readenv.str("LANGUAGE_CODE", "en")

SITE_ID = 1

USE_I18N = True
# LOCALE_PATHS = []
USE_TZ = True

MEDIA_URL = readenv.str("MEDIA_URL", "/media/")
MEDIA_ROOT = readenv.str("MEDIA_ROOT", var_rel("media"))
STATIC_URL = readenv.str("STATIC_URL", "/static/")
STATIC_ROOT = readenv.str("STATIC_ROOT", var_rel("static"))

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # lib_rel('django', 'contrib', 'admin', 'static'),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STORAGES = {
    "default": readenv.str("DEFAULT_BACKEND_STORAGE", "fs://"),
    "staticfiles": readenv.str("STATICFILES_BACKEND_STORAGE", "whitenoise+static://"),
}
FILE_UPLOAD_PERMISSIONS = 0o644

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
            # rel("templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # "django.template.context_processors.csrf",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",{% if cookiecutter.project_type == "django-cms" %}
                "cms.context_processors.cms_settings",{% endif %}
                "sekizai.context_processors.sekizai",
            ],
            # "loaders": [
            #     "django.template.loaders.filesystem.Loader",
            #     "django.template.loaders.app_directories.Loader",
            # ],
            # "builtins": [
            # ],
        },
    }
]

MIDDLEWARE = [
    # "django.middleware.cache.UpdateCacheMiddleware",  # enable cache{% if cookiecutter.project_type == "django-cms" %}
    "cms.middleware.utils.ApphookReloadMiddleware",{% endif %}
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # "django.middleware.http.ConditionalGetMiddleware",
    # "django.middleware.gzip.GZipMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",{% if cookiecutter.project_type == "django-cms" %}
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",{% endif %}
    # "django.middleware.cache.FetchFromCacheMiddleware",  # enable cache
]
INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = readenv.str("ROOT_URLCONF", "{{ cookiecutter.project_name }}.urls")
# LOGIN_URL = reverse_lazy("login")
# LOGOUT_URL = reverse_lazy("logout")
# LOGIN_REDIRECT_URL = "/"  # "/accounts/profile/"
AUTH_USER_MODEL = "auth.User"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = readenv.str("WSGI_APPLICATION", "{{ cookiecutter.project_name }}.wsgi.application")

INSTALLED_APPS = [
    "{{ cookiecutter.project_name }}.apps.{{ cookiecutter.camel_case_app_name }}Config",
    {% if cookiecutter.use_postgresql == "y" %}"django.contrib.postgres.apps.PostgresConfig",
    {% endif %}"django.contrib.auth.apps.AuthConfig",
    "django.contrib.contenttypes.apps.ContentTypesConfig",
    "django.contrib.sessions.apps.SessionsConfig",
    "django.contrib.sites.apps.SitesConfig",
    "django.contrib.messages.apps.MessagesConfig",
    "django.contrib.staticfiles.apps.StaticFilesConfig",
    "whitenoise.runserver_nostatic",
    "{{ cookiecutter.project_name }}.apps.StaticFilesConfig",
    "{{ cookiecutter.project_name }}.apps.AdminConfig",{% if cookiecutter.use_sorl_thumbnail == "y" %}
    "sorl.thumbnail",{% endif %}{% if cookiecutter.use_djangorestframework == "y" %}
    "rest_framework",
    "rest_framework.authtoken",{% endif %}
    # "classytags",
    # "sekizai",
    "{{ cookiecutter.project_name }}.apps.ClassyTagsConfig",
    "{{ cookiecutter.project_name }}.apps.SekizaiConfig",{% if cookiecutter.use_widget_tweaks == "y" or cookiecutter.project_type == "django-cms" %}
    # widget_tweaks
    "{{ cookiecutter.project_name }}.apps.WidgetTweaksConfig",{% endif %}{% if cookiecutter.project_type == "django-cms" %}
    "mptt",
    "treebeard",
    "djangocms_text_ckeditor", # note this needs to be above the "cms" entry
    "menus.apps.MenusConfig",
    "easy_thumbnails",
    "formtools",
    "cms.apps.CMSConfig",
    "djangocms_column",
    "djangocms_file",
    "djangocms_googlemap",
    "djangocms_link",
    "djangocms_picture",
    "djangocms_style",
    "djangocms_video",
    "filer",{% endif %}{% if cookiecutter.use_cookielaw == "y" %}
    "legal.apps.LegalConfig",{% endif %}
]

#######################
# Password validation #
#######################

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#     },
# ]


SILENCED_SYSTEM_CHECKS = []

########################
# DJANGO DEBUG TOOLBAR #
########################

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "HIDE_DJANGO_SQL": False,
    "ENABLE_STACKTRACES": True,
}

HIDDEN_SETTINGS = sorted(
    set(
        [
            *cache_hidden_settings,
            *email_hidden_settings,
            *secret_hidden_settings,
        ]
    )
)
