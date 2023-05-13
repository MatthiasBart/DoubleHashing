#!/usr/bin/env python3

import unittest
from collections.abc import Callable
from hash import HashEntry, HashTable
import sys
import platform

print(sys.version_info)

def build_hash_table(test_data: list[(str, int)], size: int) -> HashTable:
    ht = HashTable(size)
    for (value, expected_index) in test_data:
        key = int(value)
        ht.set_key_value(expected_index, key, value)
    return ht


class HashTest(unittest.TestCase):
    def test_insert_1(self):
        test_data = [("12",5), ("53",4), ("5",3), ("15",1) , ("2",2), ("19",0), ("99", 6)]
        ht = self.check_insert(test_data, 7)
        self.assertEqual(-1, ht.insert(1, "1"), "Inserting into full table")

    def test_insert_2(self):
        test_data = [("14",1), ("21",8), ("27",2), ("28",7) , ("8",12),
                     ("18",5), ("15",10), ("36",6), ("5",0), ("2", 9)]
        self.check_insert(test_data, 13)

    def test_insert_3(self):
        # build hash table
        test_data = [("12",5), ("53",4), ("5",3), ("15",1) , ("2",2), ("19",0)]
        ht = self.check_insert(test_data, 7)
        # try to insert the same keys again
        for (value, expected_index) in test_data:
            key = int(value)
            self.assertEqual(-1, ht.insert(key, value), f"Insert of duplicate key {key} possible")

    def test_insert_brent_1(self):
        test_data = [("12",2), ("53",4), ("5",5)]
        ht = self.check_brent(test_data, 7)

    def test_insert_brent_2(self):
        test_data = [("14",6), ("21",8), ("27",1), ("28",2), ("8",3),
                     ("18",5), ("15",10), ("36",11), ("5",12), ("2",9)]
        ht = self.check_brent(test_data, 13)

    def test_retrieve(self):
        # build hash table
        test_data = [("12",5), ("53",4), ("5",3), ("15",1) , ("2",2), ("19",0)]
        ht = build_hash_table(test_data, 7)
        # retrieve all values
        for (value, expected_index) in test_data:
            key = int(value)
            self.assertEqual(value, ht.retrieve(key), f"Failed to retrieve key {key}")
            print(f"value for key {key} found")
        # test not existing key
        self.assertEqual(None, ht.retrieve(99), f"Not existing key {key} found in table")
        # test retrieve after deleted key
        ht.table[1].delete()
        self.assertEqual("5", ht.retrieve(5), f"Failed to retrieve key {key}")

    def test_delete(self):
        # build hash table
        test_data = [("12",5), ("53",4), ("5",3), ("15",1) , ("2",2), ("19",0)]
        ht = build_hash_table(test_data, 7)
        # delete every key from the table
        for (value, expected_index) in test_data:
            key = int(value)
            self.assertEqual(expected_index, ht.delete(key), f"Deleting key {key} returns wrong index")
            self.assertNotEqual(None, ht.table[expected_index], f"Deleting of key {key} sets index empty")
            self.assertEqual(None, ht.table[expected_index].key, f"Deleting of key {key} does not remove key")
            self.assertEqual(None, ht.table[expected_index].value, f"Delete of key {key} does not remove value")

    def check_insert(self, test_data: list[(str, int)], size: int) -> HashTable:
        ht = HashTable(size)
        for (value, expected_index) in test_data:
            key = int(value)
            table_index = ht.insert(key, value)
            print(f"index for key {value}: {table_index}")
            self.assertEqual(expected_index, table_index, f"index error for key {key}")
            self.assertEqual(key, ht.table[table_index].key, "key not found in table index")
            self.assertEqual(value, ht.table[table_index].value, "value not found in table index")
        return ht

    def check_brent(self, test_data: list[(str, int)], size: int) -> HashTable:
        ht = HashTable(size)
        # insert all test_data
        for (value, expected_index) in test_data:
            key = int(value)
            table_index = ht.insert_brent(key, value)
            print(f"index for key {value}: {table_index}")
        # compare data in expected positions
        for (value, expected_index) in test_data:
            key = int(value)
            self.assertEqual(key, ht.table[expected_index].key, "key not found in table index")
            self.assertEqual(value, ht.table[expected_index].value, "value not found in table index")


if __name__ == '__main__':
    unittest.main()
