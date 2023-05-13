class HashEntry:
    """
    Wrapper class for hash table entries.
    """
    def __init__(self, key: int, value: object) -> None:
        """
        Constructor for hash table entries.
        :param key: key of hash table entry
        :param value: value of hash table entry
        :return: None
        """
        self.key = key
        self.value = value

    def delete(self) -> None:
        """
        Delete the hash table entry content.
        :return: None
        """
        self.key = None
        self.value = None

    def __str__(self) -> str:
        """
        The string representation for the object is the string representation of the key.
        :return: String representation of key
        """
        return f"{self.key}"


class HashTable:
    """
    Implementation of a hash table based on Open Hashing.
    A hash entries is wrapped in a HashEntry object before being put into the list that represents the hash table:
    -  If the hash table entry is None, the entry is empty
    -  If the hash table contains a HashEntry wrapper object with a None key and value attributes, the entry is "free",
      meaning there was data that has already been deleted
    -  If the hash table contains a HashEntry wrapper object with a valid key and value attributes, the hash table entry
      is in use
    Attributes:
        table: list of HashEntry or None objects
    """
    def __init__(self, size: int):
        """
        Initialize a hash table with a given size.
        :param size: hash table size, maximum number of elements that may be stored in the hash table
        :return: None
        """
        self.table = [None] * size
        self._m = size 

    def insert(self, key: int, value: object) -> int:
        """
        Insert the given key/value entry into the hash table using double hashing (without Brent).
        :param key: the key that identifies the entry and that is used for the hash function
        :param value: value to insert with the key into the hash table
        :return: table index where the value was successfully inserted, or -1 if table is full or an entry with the
        same key already exists within the table
        """
        # Begin implementation
        hash_end = -1
        for i in range(0, self._m):
            hash = (self.hk(key, self._m) - i * self.hk2(key, self._m)) % self._m
            #check if is empty or free and insert
            if self.is_free(hash): 
                hash_end = hash
                self.set_key_value(hash, key, value)
                break
            # check if already exists 
            if self.table[hash].key == key: return -1
        # return hash_end, if not successful its -1
        return hash_end
        # End implementation

    def insert_brent(self, key: int, value: object) -> int:
        """
        Insert a given key/value entry into the hash table using double hashing with Brent.
        :param key: the key that identifies the entry and that is used for the hash function
        :param value: value to insert with the key into the hash table
        :return: table index where the object was successfully inserted, or -1 if table is full or an entry with the
        same key already exists within the table
        """
        # Begin implementation
        hash_end = -1
        for i in range(0, self._m):
            hash = (self.hk(key, self._m) - i * self.hk2(key, self._m)) % self._m
            #check if is empty or free and insert
            if self.is_free(hash): 
                hash_end = hash
                self.set_key_value(hash, key, value)
                break
            # check if already exists 
            if self.table[hash].key == key: return -1
            # check if next is free 
            hash1 = (hash - self.hk2(key, self._m)) % self._m
            if self.is_free(hash1):
                self.set_key_value(hash1, key, value)
                hash_end = hash1
                break
            # check if can move the existed away
            hash2 = (hash -  self.hk2(self.table[hash].key, self._m)) % self._m
            if self.is_free(hash2):
                self.set_key_value(hash2, self.table[hash].key, self.table[hash].value)
                self.set_key_value(hash, key, value)
                hash_end = hash
                break
        # return hash_end, if not successful its -1
        return hash_end
        # End implementation

    def retrieve(self, key: int) -> object:
        """
        Retrieve the key in the hash table and return the value object.
        :param key: the key that identifying the entry
        :return: value object if the was found in the hash table, None otherwise
        """
        # Begin implementation
        hash = self.get_position(key)
        if hash == -1: return None
        return self.table[hash].value
        # End implementation

    def delete(self, key: int) -> int:
        """
        Delete an entry from the hash table.
        :param key: key identifying the hash table entry
        :return: table index where the key was found and deleted, or -1 if the key was not found
        """
        # Begin implementation
        hash = self.get_position(key)
        if hash == -1: return -1
        self.table[hash].delete()
        return hash
        # End implementation

    def set_key_value(self, index: int, key: int, value: object):
        """
        Set a key/value entry in the hash table at the given index
        :param index: index in hash table
        :param key: key to set
        :param value: value to set
        :return:
        """
        if self.is_empty(index):
            # insert new HashEntry object at position index
            self.table[index] = HashEntry(key, value)
        else:
            # re-use existing HashEntry object
            self.table[index].key = key
            self.table[index].value = value

    def is_empty(self, index: int) -> bool:
        """
        Check if a given table index is empty, i.e. it contains None instead of a HashEntry object
        @param index: index in hash table to check
        @return: True if the table contains None at the given index, False otherwise
        """
        # check if table index is empty
        if self.table[index] is None:
            return True
        else:
            return False

    def is_free(self, index: int) -> bool:
        """
        Check if a given table index is free, i.e. either empty or it contains a deleted entry
        :param index:
        :return: True if the table index may be used for inserting, False otherwise
        """
        # If table index is empty it is free
        if self.is_empty(index):
            return True
        # If it contains a deleted entry it is also free
        if self.table[index].key is None:
            return True
        else:
            return False

    # Add your auxiliary methods here
    # Begin implementation

    def hk(self, k: int, m: int) -> int:
        if m == 0: return 0
        return k % m 
    
    def hk2(self, k: int, m: int) -> int:
        if m == 2: return 0
        return 1 + (k % (m - 2))
    
    def get_position(self, k: int) -> int:
        hash_end = -1
        for i in range(0, self._m):
            hash = (self.hk(k, self._m) - i * self.hk2(k, self._m)) % self._m 
            if self.is_free(hash): continue
            if self.table[hash].key == k: hash_end = hash; break
        return hash_end
    # End implementation

