"""
This file isolate logger configuration
"""

from collections.abc import Mapping
import logging
from typing import Any, Callable, Literal

import readenv

from ._paths import log_rel as _log_rel


def get_logging_conf(
    min_log_level: Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = None,
    *,
    log_rel: Callable[[str], str] = _log_rel,
) -> Mapping[str, Any]:
    """
    @param min_log_level set every loggers at least to this level
    """

    error_levels = {
        "NOTSET": logging.NOTSET,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    conf = _get_logging_conf(log_rel=log_rel)

    if min_log_level is None:
        return conf

    for handler in conf["handlers"].values():
        if error_levels[handler.get("level", "NOTSET")] < error_levels[min_log_level]:
            handler["level"] = min_log_level
    for logger in conf["loggers"].values():
        if error_levels[logger.get("level", "NOTSET")] < error_levels[min_log_level]:
            logger["level"] = min_log_level

    return conf


def require_debug_false_callback(*args: object, **kwargs: object) -> bool:
    from django.conf import settings

    return not settings.DEBUG


def _get_logging_conf(log_rel: Callable[[str], str]) -> Mapping[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s - %(process)5d %(pathname)s::%(funcName)s[%(lineno)d]: %(levelname)s %(message)s",  # noqa: E501
            },
            "simple": {
                "format": "[%(asctime)s] %(levelname)s %(message)s",
            },
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[%(server_time)s] %(message)s",
            },
        },
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.CallbackFilter",
                "callback": require_debug_false_callback,
            },
        },
        "handlers": {
            "null": {
                "level": readenv.str("NULL_LOG_HANDLER_LEVEL", "DEBUG"),
                "class": "logging.NullHandler",
            },
            "console": {
                "level": readenv.str("CONSOLE_LOG_HANDLER_LEVEL", "DEBUG"),
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "file": {
                "level": readenv.str("FILE_LOG_HANDLER_LEVEL", "INFO"),
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "verbose",
                "filename": log_rel("web-info.log"),
                "when": "D",
                "interval": 7,
                "backupCount": 4,
                "delay": True,
                # rotate every 7 days, keep 4 old copies
            },
            "error_file": {
                "level": readenv.str("ERROR_FILE_LOG_HANDLER_LEVEL", "ERROR"),
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "verbose",
                "filename": log_rel("web-error.log"),
                "when": "D",
                "interval": 7,
                "backupCount": 4,
                "delay": True,
                # rotate every 7 days, keep 4 old copies
            },
            "mail_admins": {
                "level": readenv.str("MAIL_ADMINS_LOG_HANDLER_LEVEL", "ERROR"),
                "class": "django.utils.log.AdminEmailHandler",
                "include_html": True,
                "filters": ["require_debug_false"],
            },
            "django.server": {
                "level": readenv.str("DJANGO_SERVER_LOG_HANDLER_LEVEL", "INFO"),
                "class": "logging.StreamHandler",
                "formatter": "django.server",
            },
            "worker-lead": {
                "level": readenv.str("WORKER_LEAD_LOG_HANDLER_LEVEL", "INFO"),
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "verbose",
                "filename": log_rel("worker-lead.log"),
                "when": "D",
                "interval": 7,
                "backupCount": 4,
                "delay": True,
                # rotate every 7 days, keep 4 old copies
            },
            "worker-sdi": {
                "level": readenv.str("WORKER_SDI_LOG_HANDLER_LEVEL", "INFO"),
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "verbose",
                "filename": log_rel("worker-sdi.log"),
                "when": "D",
                "interval": 7,
                "backupCount": 4,
                "delay": True,
                # rotate every 7 days, keep 4 old copies
            },
        },
        "loggers": {
            "django": {
                # django is the catch-all logger. No messages are posted directly to this logger.
                "handlers": ["null", "error_file"],
                "propagate": True,
                "level": readenv.str("DJANGO_LOG_LEVEL", "INFO"),
            },
            "django.request": {
                "handlers": ["error_file", "mail_admins"],
                "level": readenv.str("DJNGO_REQUEST_LOG_LEVEL", "ERROR"),
                "propagate": False,
            },
            "django.server": {
                "handlers": ["django.server"],
                "level": readenv.str("DJANGO_SERVER_LOG_LEVEL", "INFO"),
                "propagate": False,
            },
            "gunicorn.error": {
                "level": readenv.str("GUNICORN_ERROR_LOG_LEVEL", "DEBUG"),
                "handlers": ["console"],
                "propagate": True,
            },
            "gunicorn.access": {
                "level": readenv.str("GUNICORN_ACCESS_LOG_LEVEL", "DEBUG"),
                "handlers": ["console"],
                "propagate": False,
            },
            "web": {
                "handlers": ["console", "file", "error_file", "mail_admins"],
                "level": readenv.str("WEB_LOG_LEVEL", "INFO"),
            },
            "worker-lead": {
                "handlers": ["console", "file", "worker-lead", "error_file", "mail_admins"],
                "level": readenv.str("WORKER_LEAD_LOG_LEVEL", "INFO"),
            },
            "worker-sdi": {
                "handlers": ["console", "file", "worker-sdi", "error_file", "mail_admins"],
                "level": readenv.str("WORKER_SDI_LOG_LEVEL", "INFO"),
            },
        },
    }


# default logging configuration
LOGGING = get_logging_conf()

# keep always as last item
__all__ = [key for key in locals().keys() if key.isupper()] + ["get_logging_conf"]
