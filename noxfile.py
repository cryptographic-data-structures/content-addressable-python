#  Copyright (c) 2022. VMware, Inc.
#  SPDX-License-Identifier: Apache-2.0
import os
import unittest

import nox


@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8', '--verbose', 'content_addressable')


@nox.session
def tests(session):
    session.install('-e', '.')
    session.install('-r', 'test-requirements.txt')
    session.run(
        'python3',
        '-m',
        'unittest',
        'discover',
        '--start-directory',
        'tests',
        '-p',
        '*_test*.py',
        )
