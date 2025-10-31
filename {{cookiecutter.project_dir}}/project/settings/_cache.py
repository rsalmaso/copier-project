import readenv

CACHES = {
    "default": readenv.str("DEFAULT_CACHE", "memory://"),
}
# CACHE_MIDDLEWARE_KEY_PREFIX = ""
# CACHE_MIDDLEWARE_SECONDS = 600
# CACHE_MIDDLEWARE_ALIAS = "default"

# keep always export_settings, cache_hidden_settings and __all__ as last items
# cache_hidden_settings is merged into HIDDEN_SETTINGS and used by project.debug.ExceptionReporterFilter
export_settings = [key for key in locals().keys() if key.isupper()]
cache_hidden_settings = ["CACHES"]
__all__ = export_settings + ["cache_hidden_settings"]
