#!/usr/bin/env -S uv run --script --quiet

# Copyright (C) Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "python-readenv>=0.7.1",
#     "rich>=14.2.0",
# ]
# ///

import contextlib
import glob
import os
import random
import shutil
import subprocess
import time

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
print(PROJECT_DIRECTORY)


@contextlib.contextmanager
def cd(VENV_PATH):
    cwd = os.getcwd()
    os.chdir(VENV_PATH)
    yield
    os.chdir(cwd)


def system(*args, **kwargs):
    env = kwargs.pop("env", None)
    return subprocess.call(list(args), env=env)


class Project:
    def mkdir(self, directory) -> None:
        system(
            "mkdir",
            "-p",
            os.path.join(PROJECT_DIRECTORY, directory),
        )

    def rmdir(self, path: str) -> None:
        path = os.path.join(PROJECT_DIRECTORY, path)
        if os.path.exists(path):
            shutil.rmtree(path)

    def add(self, *, pkg: str, group: str = "") -> None:
        if group:
            system("uv", "add", "--group", group, pkg)
        else:
            system("uv", "add", pkg)

    def sync(self):
        system("uv", "sync")

    def collectstatic(self):
        system(
            "uv",
            "run",
            "python",
            os.path.join(PROJECT_DIRECTORY, "manage.py"),
            "collectstatic",
            "--noinput",
        )


def get_random_string(
    length=50, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789!@#%^&*(-_=+)"
):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    # if not using_sysrandom:
    ## This is ugly, and a hack, but it makes things better than
    ## the alternative of predictability. This re-seeds the PRNG
    ## using a value that is hard for an attacker to predict, every
    ## time a random string is required. This may change the
    ## properties of the chosen random sequence slightly, but this
    ## is better than absolute predictability.
    # random.seed(
    # hashlib.sha256(
    # ("%s%s%s" % (
    # random.getstate(),
    # time.time(),
    # settings.SECRET_KEY)).encode('utf-8')
    # ).digest())
    return "".join(random.choice(allowed_chars) for i in range(length))


def set_secret_key(setting_file_location):
    # Open locals.py
    with open(setting_file_location) as f:
        file_ = f.read()

    # Generate a SECRET_KEY that matches the Django standard
    SECRET_KEY = get_random_string()

    # Replace "CHANGEME!!!" with SECRET_KEY
    file_ = file_.replace("<%SECRET_KEY%>", SECRET_KEY, 1)

    # Write the results to the locals.py module
    with open(setting_file_location, "w") as f:
        f.write(file_)


def make_secret_key(project_directory):
    """Generates and saves random secret key"""
    return
    # Determine the local_setting_file_location
    set_secret_key(
        os.path.join(
            project_directory,
            "{{ cookiecutter.project_name }}",
            "project",
            "settings",
            "local.py",
        )
    )

    set_secret_key(
        os.path.join(
            project_directory,
            "{{ cookiecutter.project_name }}",
            "project",
            "settings",
            "base.py",
        )
    )


def remove_working_files():
    pass
    # os.remove(os.path.join(PROJECT_DIRECTORY, "COPYING.py"))


def uv_add(project: Project, group: str = "") -> None:
    filename = f"requirements.{group}.in" if group else "requirements.in"
    path = os.path.join(PROJECT_DIRECTORY, "_requirements", filename)
    print(f"{path=}")
    with open(path) as f:
        for line in f.readlines():
            line = line.replace("\n", "").strip()
            print(f"line: {line!r}")
            if line and not line.startswith("#"):
                project.add(pkg=line, group=group)


def init():
    # make_secret_key(PROJECT_DIRECTORY)

    project = Project()

    uv_add(project)
    uv_add(project, "dev")
    uv_add(project, "ci")

    project.rmdir("_requirements")
    # remove_working_files()
    # project.collectstatic()
    # sys.exit(0)


init()
