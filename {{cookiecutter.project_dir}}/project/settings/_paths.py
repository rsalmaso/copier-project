import pathlib

import readenv

PROJECT_PATH: str = str(pathlib.Path(__file__).parent.parent.parent)


def rel(*args: str) -> str:
    return str(pathlib.Path(PROJECT_PATH).joinpath(*args).resolve())


VAR_DIR: str = readenv.str("VAR_DIR", rel("var"))


def var_rel(*args: str) -> str:
    return str(pathlib.Path(VAR_DIR).joinpath(*args).resolve())


LOG_DIR: str = readenv.str("LOG_DIR", var_rel("log"))


def log_rel(*args: str) -> str:
    return str(pathlib.Path(LOG_DIR).joinpath(*args).resolve())


# keep always as last item
__all__ = [key for key in locals().keys() if key.isupper()] + ["rel", "var_rel", "log_rel"]
