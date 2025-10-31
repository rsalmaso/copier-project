import re

from django.conf import settings
from django.views import debug as debug_view


class ExceptionReporterFilter(debug_view.SafeExceptionReporterFilter):
    @property
    def hidden_settings(self):
        return re.compile(
            "|".join([super().hidden_settings.pattern, *settings.HIDDEN_SETTINGS]),
            flags=re.IGNORECASE,
        )
