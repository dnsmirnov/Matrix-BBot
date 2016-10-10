#!/usr/bin/env python
from setuptools import setup

setup(
    name="Matrix-BB",
    version="0.0.1",
    description="Bingo-Boom bot for Matrix",
    author="Dmitriy Smirnov",
    author_email="dn_smirnov@bingo-boom.ru",
    url="https://github.com/dnsmirnov/Matrix-BBot",
    packages = ['bbot', 'plugins','matrix_client'],
    license = "LICENSE",
    install_requires = [
        "matrix_client",
        "Flask",
        "python-dateutil"
    ],
    dependency_links=[
        "https://github.com/matrix-org/matrix-python-sdk/"
    ]
)
