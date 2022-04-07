#  Copyright (c) 2022. VMware, Inc.
#  SPDX-License-Identifier: Apache-2.0

import unittest

from content_addressable.data import Memo, MemoTamperError


class DataTestCase(unittest.TestCase):
    def test_simple_tamper_detection(self):
        data = Memo.create(dict(foo='bar'))
        self.assertIsNotNone(data)
        self.assertIsNotNone(data.cid())
        dup = data.copy()
        self.assertIsNotNone(dup)
        self.assertEqual(data.multihash(), dup.multihash())
        self.assertEqual(data.cid(), dup.cid())
        dup['foo'] = 'bad'
        self.assertNotEqual(data.multihash(), dup.multihash())
        self.assertNotEqual(data.cid(), dup.cid())

    def test_tamper_exception(self):
        data = Memo(dict(foo='bar', data={'safe': True}))
        self.assertTrue(data['data']['safe'])
        data['data']['safe'] = False
        self.assertRaises(
            MemoTamperError,
            lambda: data['data']['safe']
        )


if __name__ == '__main__':
    unittest.main()
