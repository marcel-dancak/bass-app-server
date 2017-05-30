#!/usr/bin/env python

import os
from setuptools import setup, find_packages


# classifiers
classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License version 2.0 (GPLv2)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Multimedia :: Sound/Audio',
]

exclude_from_packages = [
    'basscloud.catalog.migrations',
    'basscloud.feedback.migrations',
    # 'basscloud.conf.project_template'
]

# requirements
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# setup
setup(name='basscloud',
    version=(__import__('basscloud').VERSION),
    description='BassCloud Server',
    author='Marcel Dancak',
    author_email='dancakm@gmail.com',
    url='https://github.com/marcel-dancak/bass-cloud',
    packages=find_packages('./', exclude=exclude_from_packages),
    include_package_data=True,
    classifiers=classifiers,
    install_requires=requirements
)

# vim: set ts=8 sts=4 sw=4 et:
