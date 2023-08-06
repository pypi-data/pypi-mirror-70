#!/usr/bin/env python3
import os
from setuptools import setup

PKG_NAME = "taskw_gcal_sync"

AUTHOR = "Nikos Koukis"
AUTHOR_EMAIL = "nickkouk@gmail.com"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name=PKG_NAME,
    version="0.4.3",
    description="Taskwarrior <-> Google Calendar synchronisation tool",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="BSD 3-clause",
    install_requires=(
        "arrow",
        "bidict",
        "click",
        "colorlog",
        "google-api-python-client",
        "google-auth-oauthlib",
        "mypy",
        "overrides",
        "pytz",
        "pyyaml",
        "rfc3339",
        "sh",
        "taskw",
        "typing",
    ),
    url="https://github.com/bergercookie/{}".format(PKG_NAME),
    download_url="https://github.com/bergercookie/{}".format(PKG_NAME),
    dependency_links=[],
    scripts=["tw_gcal_sync"],
    packages=[PKG_NAME],
    test_suite="test",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    package_data={PKG_NAME: ["res/gcal_client_secret.json"]},
)
