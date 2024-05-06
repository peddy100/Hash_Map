# Name: Pedram Jarahzadeh
# OSU Email: jarahzap@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/2/2022
# Description: Implement the HashMap class using a dynamic array to store the hash table and Open Addressing
# with Quadratic Probing for collision resolution inside that dynamic array. Includes put(), get(), remove(),
# contains_key(), clear(), empty_buckets(), resize_table(), table_load(), get_keys(), and find_mode() methods

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the key exists it updates the value, otherwise it adds a new
        key/value pair

        :param key: A string representing the key in the key value pair
        :param value: An object representing the object in the key value pair

        :return: None
        """
        # Resize the table to twice the capacity if the table load is greater than 1.0
        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        for i in range(0, self._capacity):
            # Initialize the hash and index
            hash = self._hash_function(key)
            index = (hash + i ** 2) % self._capacity

            # Check if the table contains the key. If so update the value.
            if self._buckets[index] is not None and self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                self._buckets[index].value = value
                return

            # Otherwise add a new key/value pair and increment the size
            elif self._buckets[index] is None or self._buckets[index].is_tombstone is True:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return

    def table_load(self) -> float:
        """
        Calculates the current hash table load factor.

        :param: None

        :return: A float representing the table load factor.
        """
        # Use 𝝺 = n/m to calculate load
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Calculates the number of empty buckets in the hash table

        :param: None

        :return: An integer representing the number of empty buckets in the table
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table while maintaining and rehashing the existing key/value pairs

        :param new_capacity: An integer representing desired capacity for the hash table

        :return: None
        """
        # Do nothing if the desired capacity is less than the table size
        if new_capacity < self._size:
            return

        # Save the old hash map
        hash_map = self._buckets

        # Update the desired capacity to a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Set the capacity and clear the hash table
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        self._size = 0
        for i in range(self._capacity):
            self._buckets.append(None)

        # Rehash the elements
        for i in range(0, hash_map.length()):
            if hash_map[i] is not None and hash_map[i].is_tombstone is False:
                self.put(hash_map[i].key, hash_map[i].value)

    def get(self, key: str) -> object:
        """
        Finds the value in the hash table when passed a key

        :param key: A string representing the key to find in the hash table

        :return: An object representing the value corresponding to the found key or None if the key doesn't exist
        """

        for i in range(0, self._capacity):
            # Initialize hash and index
            hash = self._hash_function(key)
            index = (hash + i ** 2) % self._capacity

            # Check if hashmap contains the key. Return the value if key is found
            if self._buckets[index] is not None and self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                return self._buckets[index].value

        # Else return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines is a given key is in the hash table

        :param key: A string representing the key to find

        :return: A boolean representing if the key is found
        """
        for i in range(0, self._capacity):
            # Initialize hash and index
            hash = self._hash_function(key)
            index = (hash + i ** 2) % self._capacity

            # Check if key is in the hashmap
            if self._buckets[index] is not None and self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                return True

        # Else return False
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map,
        otherwise does nothing if the key doesn't exist.

        :param key: A string representing the key to find

        :return: None
        """
        for i in range(0, self._capacity):
            # Initialize hash and index
            hash = self._hash_function(key)
            index = (hash + i ** 2) % self._capacity

            # Set Tombstone to True if found otherwise do nothing
            if self._buckets[index] is not None and self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                self._buckets[index].is_tombstone = True
                self._size -= 1
        return

    def clear(self) -> None:
        """
        Clears the contents of the hash map while maintaining the capacity.

        :param: None

        :return: None
        """
        # Reinitialize buckets to None
        for i in range(0, self._capacity):
            self._buckets[i] = None

        # Reset size to zero
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map

        :param: None

        :return: A Dynamic array in which each index contains a tuple of a key/value pair
        stored in the hash map
        """
        # Create a new Dynamic Array to return
        return_array = DynamicArray()

        # Add Tuples containing key value pairs to the array and return the array
        for i in range(0, self._capacity):
            if self._buckets[i] is not None and self._buckets[i].is_tombstone is False:
                return_array.append((self._buckets[i].key, self._buckets[i].value))
        return return_array

    def __iter__(self):
        """
        TODO: Write this implementation
        """
        self._index = 0

        return self

    def __next__(self):
        """
        TODO: Write this implementation
        """

        if self._buckets[self._index] is not None:
            try:
                value = self._buckets[self._index]
            except DynamicArrayException:
                raise StopIteration

        self._index += 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
