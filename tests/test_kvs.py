import unittest

from kvs.kvs import KeyValueStore


class TestKeyValueStore(unittest.TestCase):

    def setUp(self):
        self.kvs = KeyValueStore()

    def test_set(self):
        self.assertTrue(self.kvs.set('a', 'b'))

    def test_get(self):
        self.kvs.set('a', 'b')
        self.assertEqual(self.kvs.get('a'), 'b')
        self.assertEqual(self.kvs.get('z'), None)

    def test_delete(self):
        self.kvs.set('a', 'b')
        self.assertTrue(self.kvs.delete('a'))
        self.assertFalse(self.kvs.delete('a'))