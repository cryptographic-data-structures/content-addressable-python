#  Copyright (c) 2022. VMware, Inc.
#  SPDX-License-Identifier: Apache-2.0

import io
import os

from setuptools import find_packages, setup


# custom read implementation here allows me to use the VERSION file
# as a way to control the version number. Alternatively, I have used
# git tag names to control version release numbers. In this case
# I'm not presupposing an automated release pipeline.
def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


VERSION = str(read('VERSION')).strip()
packages = [item for item in find_packages(
    './*', exclude=['tests']) if not str(item).startswith('test')]

setup(
    name='content-addressable',
    version=VERSION,
    description='content-addressable data structures',
    author='Shawn Hartsock',
    author_email='hartsocks@vmware.com',
    packages=packages,

    # we include the fixture data files in the test harness in the packages for
    # source distributions
    package_data={
        '': ['*.yml', '*.yaml', '*.txt', '*.json'],
        'tests/fixtures': ['*.*']
    },
    # we scoop the installer requirements into the packager's definition here
    install_requires=read('requirements.txt').splitlines(),

    # package classifiers for full-featured PyPi search engines help SEO for
    # the package and increase its chances of getting noticed by a Linux
    # Distribution maintainer, they will fork and create their own RPM and
    # DEB packages for us.
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # testing suites are broken out into their own requirements file
    test_suite='test',
    tests_require=read('test-requirements.txt').splitlines(),

    # This is a library and/or CLI tool and we specify the executable entry
    # point for the packager by using this setting here to indicate what method
    # it should call if installed in a linux distribution's /usr/local/bin
    entry_points={
        'console_scripts': [
            # 'conadr = content_addressable.__main__:main',
        ]
    },
)
