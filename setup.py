#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import sys
if sys.version_info < (2, 6):
    print("THIS MODULE REQUIRES PYTHON 2.6, 2.7, OR 3.3+. YOU ARE CURRENTLY USING PYTHON {0}".format(sys.version))
    sys.exit(1)

import ImEverywhere

setup(
    name = "ImEverywhere",
    version = ImEverywhere.__version__,
    packages = ["ImEverywhere"],
    include_package_data = True,

    # PyPI metadata
    author = ImEverywhere.__author__,
    author_email = "1044908508@qq.com",
    description = ImEverywhere.__doc__,
    long_description = open("README.rst").read(),
    license = ImEverywhere.__license__,
    keywords = "ImEverywhere NLP MachineLearning",
    url = "https://github.com/decalogue/ImEverywhere",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
		"Natural Language :: Chinese",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Other OS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: MachineLearning :: NLP :: ChatRobot",
    ],
)
