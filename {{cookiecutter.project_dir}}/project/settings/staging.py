import readenv

readenv.setdefault("ENV", "staging")

from .base import *  # noqa: E402,F401,F403
