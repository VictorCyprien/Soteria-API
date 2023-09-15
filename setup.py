#!/usr/bin/env python3
from setuptools import setup, find_packages

required = [
    "apispec",
    "aiohttp",
    "aiohttp_apispec",
    "colorlog",
    "gunicorn",
    "pandas",
    "requests",
    "environs"
]

VERSION = "2023.09.13"

setup(
      name='soteria-api',
      version=VERSION,
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=required,
)
