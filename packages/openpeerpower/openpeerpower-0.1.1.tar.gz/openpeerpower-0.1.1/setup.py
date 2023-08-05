#!/usr/bin/env python3
"""Open Peer Power setup script."""
from datetime import datetime as dt
from setuptools import find_packages, setup

import openpeerpower.const as opp_const

PROJECT_NAME = 'Open Peer Power'
PROJECT_PACKAGE_NAME = 'openpeerpower'
PROJECT_LICENSE = 'Apache License 2.0'
PROJECT_AUTHOR = 'Paul Caston'
PROJECT_COPYRIGHT = ' 2020-{}, {}'.format(dt.now().year, PROJECT_AUTHOR)
PROJECT_URL = 'https://OpenPeerPower.io/'
PROJECT_EMAIL = 'paul@caston.id.au'

PROJECT_GITHUB_USERNAME = "OpenPeerPower"
PROJECT_GITHUB_REPOSITORY = "Open-Peer-Power"

PYPI_URL = "https://pypi.python.org/pypi/{}".format(PROJECT_PACKAGE_NAME)
GITHUB_PATH = "{}/{}".format(PROJECT_GITHUB_USERNAME, PROJECT_GITHUB_REPOSITORY)
GITHUB_URL = "https://github.com/{}".format(GITHUB_PATH)

PROJECT_URLS = {
    "Bug Reports": "{}/issues".format(GITHUB_URL)
}

PACKAGES = find_packages(exclude=["tests", "tests.*"])

REQUIRES = [
    "aiohttp==3.6.1",
    "astral==1.10.1",
    "async_timeout==3.0.1",
    "attrs==19.3.0",
    "bcrypt==3.1.7",
    "certifi>=2019.11.28",
    "importlib-metadata==0.23",
    "jinja2>=2.10.3",
    "PyJWT==1.7.1",
    # PyJWT has loose dependency. We want the latest one.
    "cryptography==2.8",
    "pip>=8.0.3",
    "python-slugify==4.0.0",
    "pytz>=2019.03",
    "pyyaml==5.2.0",
    "requests==2.22.0",
    "ruamel.yaml==0.15.100",
    "voluptuous==0.11.7",
    "voluptuous-serialize==2.3.0",
]

MIN_PY_VERSION = ".".join(map(str, opp_const.REQUIRED_PYTHON_VER))

setup(
    name=PROJECT_PACKAGE_NAME,
    version=opp_const.__version__,
    url=PROJECT_URL,
    project_urls=PROJECT_URLS,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRES,
    python_requires='>={}'.format(MIN_PY_VERSION),
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'opp = openpeerpower.__main__:main'
        ]
    },
)
