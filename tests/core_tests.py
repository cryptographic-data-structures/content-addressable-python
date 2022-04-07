#  Copyright (c) 2022. VMware, Inc.
#  SPDX-License-Identifier: Apache-2.0

import unittest

from parameterized import parameterized

from content_addressable import core

TEST_VALUES = [
        [True],
        [None],
        [100],
        [';"{[!&~`\'{;\\'],
        [{'foo': 'bar'}],
        ['foo'],
        [{'foo', 'bar'}],
        [(1, 3, 7, 10, 10)],
        [[
            [{'foo', 'bar'}],
            [{'foo', 'bar'}],
            [{'foo', 'bar'}],
            [{'foo', 'bar'}]
        ]],
        [frozenset({1, 2, 3})],
    ]


class CoreTestCase(unittest.TestCase):
    report = {}

    @parameterized.expand(TEST_VALUES)
    def test_basic_encoding(self, value):
        value_id = core.content_id(value)
        self.report[value_id] = value
        # checking determinism in encoding / decoding
        self.assertEqual(value_id, core.content_id(value))
        self.assertNotEqual(value_id, core.content_id(value_id))

    @parameterized.expand(TEST_VALUES)
    def test_mapping_values(self, value):
        value_id = core.content_id(value)
        stored_value = self.report[value_id]
        self.assertEqual(value, stored_value)


if __name__ == '__main__':
    unittest.main()
