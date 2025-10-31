import readenv

readenv.setdefault("ENV", "production")

from .base import *  # noqa: E402,F401,F403
