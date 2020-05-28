# -*- coding: utf-8 -*-

import base64
import pickle
import sys


class BoxKeyError(Exception):
    pass


class BoxKeyValidationError(Exception):
    pass


class BoxUnknownKeyError(Exception):
    pass

class Box:
    def __init__(self):
        self._dict = {}

    def __iter__(self):
        return self._dict.__iter__()

    def _key_validation(self, key):
        """
        Validates that key satisfies constraints of the Box class.

        >>> b = Box()
        >>> b._key_validation("alpha") # lacks namespace
        False
        >>> b._key_validation("alpha.beta")
        True
        >>> b._key_validation("alpha0.beta0.gamma0")
        True
        >>> b._key_validation("Alpha") # Upper and lacks namespace
        False
        >>> b._key_validation("0") # Starts with digit
        False
        >>> b._key_validation("0alpha") # Starts with digit
        False
        >>> b._key_validation("0.Alpha") # Starts with digit
        False
        """
        if not isinstance(key, str):
            raise BoxKeyError("keys must be strings")
        if key[0].isdigit():
            return False
        elif key[0].isupper():
            return False
        elif len(key.split(".")) < 2:
            return False
        return True

    def insert_item(self, key, value):
        """
        Inserts item into box and associates given key with given value.

        >>> b = Box()
        >>> bads = [("alpha", 1), ("Alpha", 1), ("0alpha", 1)]
        >>> for item in bads: 
        ...     try: 
        ...         b.insert_item(item[0], item[1]) 
        ...     except BoxKeyValidationError as e: 
        ...         print(f"{item[0]}: {e}")
        alpha: key failed validation
        Alpha: key failed validation
        0alpha: key failed validation
        >>> b.insert_item("alpha.beta", 1)
        True
        >>> b.insert_item("alpha.beta.gamma", 1)
        True
        >>> b.insert_item("alpha.beta.gamma.delta", 1)
        True
        """
        if not self._key_validation(key):
            raise BoxKeyValidationError("key failed validation")
        if key in self._dict:
            raise BoxKeyError("insert does not permit update of keys")
        self._dict[key] = value
        return True

    def update_item(self, key, value):
        """
        Updates already existing item in the box, associating new value with
        existing key.

        >>> b = Box()
        >>> b.insert_item("alpha.beta", 0)
        True
        >>> b.update_item("alpha.beta", -1)
        True

        Missing item should raise an exception here.
        >>> try: 
        ...     b.update_item("alpha.beta0", -1)
        ... except BoxKeyError as e:
        ...     print(e)
        cannot update item not already in box
        """
        if not key in self._dict:
            raise BoxKeyError("cannot update item not already in box")
        if self._key_validation(key):
            self._dict[key] = value
            return True
        else:
            raise BoxKeyValidationError("key missing namespace")

    def get(self, key):
        """
        Returns value from box associated with a given key. Returns None if
        item with given key is not already in the box.

        >>> b = Box()
        >>> pairs = [("a.0", 1), ("a.1", 3), ("a.2", 7), ("a.3", 9)]
        >>> [b.insert_item(k, v) for k, v in pairs]
        [True, True, True, True]
        >>> [b.get(k) for (k, _) in pairs]
        [1, 3, 7, 9]
        """
        if not key in self._dict:
            raise BoxUnknownKeyError("Given key does not exist in this box", {"unknown_key": key})
        return self._dict[key]

    def rename_key(self, oldkey, newkey):
        """
        Renames key in the box 'oldkey' to new name 'newkey'; does not
        affect value.

        >>> b = Box()
        >>> pairs = [("a.0", 1), ("a.1", 3), ("a.2", 7), ("a.3", 9)]
        >>> [b.insert_item(k, v) for k, v in pairs]
        [True, True, True, True]
        >>> [b.rename_key(k, f"n_{k}") for (k, _) in pairs]
        [True, True, True, True]
        >>> b.tuples
        [('n_a.0', 1), ('n_a.1', 3), ('n_a.2', 7), ('n_a.3', 9)]
        """
        if not oldkey in self._dict:
            raise BoxKeyError("cannot rename non-existing key")
        if self._key_validation(newkey):
            self._dict[newkey] = self._dict[oldkey]
            del self._dict[oldkey]
            return True

    def remove_item(self, key):
        """
        Removes item from box associated with given key.

        >>> b = Box()
        >>> pairs = [("a.0", 1), ("a.1", 3), ("a.2", 7), ("a.3", 9)]
        >>> for k, v in pairs:
        ...     try:
        ...         b.remove_item(k)
        ...     except BoxKeyError as e:
        ...         print(f"{k}: {e}")
        a.0: cannot remote non-existing key
        a.1: cannot remote non-existing key
        a.2: cannot remote non-existing key
        a.3: cannot remote non-existing key
        """
        if not key in self._dict:
            raise BoxKeyError("cannot remote non-existing key")
        del self._dict[key]
        return True

    @property
    def tuples(self):
        """
        Returns a sequence of (key, value) tuples currently in the box.

        >>> b = Box()
        >>> [b.insert_item(k, v) for k, v in 
        ... [("a.0", 1), ("a.1", 3), ("a.2", 7), ("a.3", 9)]]
        [True, True, True, True]
        >>> b.tuples
        [('a.0', 1), ('a.1', 3), ('a.2', 7), ('a.3', 9)]
        """
        return [i for i in self._dict.items()]

    @property
    def keys(self):
        """
        Returns a sequence of keys currently in the box.
        >>> b = Box()
        >>> b.keys
        dict_keys([])
        >>> b.insert_item('a.b', 1)
        True
        >>> b.insert_item('c.d', 2)
        True
        >>> b.insert_item('e.f', 3)
        True
        >>> b.keys
        dict_keys(['a.b', 'c.d', 'e.f'])
        """
        return self._dict.keys()

    def dump(self):
        """
        Dumps a base64 encoded value of pickled contents of the box.

        >>> b = Box()
        >>> pairs = [("alpha.beta.0", 1), ("alpha.beta.1", 2),
        ... ("alpha.beta.3", 2)]
        >>> [b.insert_item(k, v) for k, v in pairs]
        [True, True, True]
        >>> b.dump()
        b'gAN9cQAoWAwAAABhbHBoYS5iZXRhLjBxAUsBWAwAAABhbHBoYS5iZXRhLjFxAksCWAwAAABhbHBo\\nYS5iZXRhLjNxA0sCdS4=\\n'
        """
        return base64.encodebytes(pickle.dumps(self._dict))

    def load(self, b):
        """
        Loads a base64 encoded value of pickled contents of the box.

        >>> b = Box()
        >>> b.load(b'gAN9cQAoWAwAAABhbHBoYS5iZXRhLjBxAUsBWAwAAABhbHBoYS5iZXRhLjFxAksCWAwAAABhbHBo\\nYS5iZXRhLjNxA0sCdS4=\\n')
        True
        >>> b.tuples
        [('alpha.beta.0', 1), ('alpha.beta.1', 2), ('alpha.beta.3', 2)]
        """
        unpacked = pickle.loads(base64.decodebytes(b))
        if unpacked:
            self._dict = unpacked
            return True
        return False


if __name__ == "__main__":
    # When this module is executed directly with Python interpreter, ie.:
    # > python box.py
    # We run tests described in the docstrings of the Box class methods.
    import doctest

    doctest.testmod()
