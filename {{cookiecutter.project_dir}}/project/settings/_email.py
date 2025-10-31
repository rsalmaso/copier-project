import readenv

EMAIL_BACKEND = readenv.str("EMAIL_BACKEND", "console://")
# DEFAULT_FROM_EMAIL = "webmaster@localhost"
# EMAIL_SUBJECT_PREFIX = "[Django] "
# SERVER_EMAIL = "root@localhost"

# keep always export_settings, email_hidden_settings and __all__ as last items
# email_hidden_settings is merged into HIDDEN_SETTINGS and used by project.debug.ExceptionReporterFilter
export_settings = [key for key in locals().keys() if key.isupper()]
email_hidden_settings = [
    "EMAIL_BACKEND",
    "EMAIL_HOST",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
    "EMAIL_SSL_CERTIFICATE",
    "EMAIL_SSL_KEYFILE",
    "EMAIL_SUBJECT_PREFIX",
]
__all__ = export_settings + ["email_hidden_settings"]
