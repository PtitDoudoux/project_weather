#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import weather

setup(

    name='weather',

    version="1.0",

    packages=find_packages(),

    author="Thomas DUDOUX, Gurnavdeep SINGH, Alexandre TING",

    author_email="",

    description="Print the weather of a given city",

    long_description=open('README.md').read(),

    install_requires= ["fire", "requests", "beautifulsoup4", "pytest",
                       "PyOpenGL", "PyOpenGL_accelerate", "PyQt5"],

    include_package_data=True,

    url='https://github.com/PtitDoudoux/project_weather',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Schooled",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6.1",
        "Topic :: Weather",
    ],

    entry_points={
        'console_scripts': [
            'weather = weather.weather:main',
        ],
    },

    license="WTFPL",

)