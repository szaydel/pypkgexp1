# -*- coding: utf-8 -*-
import unittest

from pypkgexp1.lib.box import Box, BoxKeyError, BoxKeyValidationError, BoxUnknownKeyError

# Main is an entrypoint used by setuptools to tie the name of wrapper script
# that it creates for our Command Line program without the ``.py`` extension to
# the code we would normally want to run the program was invoked. This assumes
# that we are building a command line utility and not just a library.
# If we are only building and packing a library, this is unnecessary.
# We should not have any business logic here, that belongs in the library. This
# makes testing easier in general, because it reduces or eliminates any need to
# test the main entrypoint.
#
# When this main_func is called, it is effectively referenced as:
# pypkgexp1.cli.main_func.
def main_func():
    b = Box()
    b.insert_item("letter.alpha", "α")
    b.insert_item("letter.beta", "β")
    b.insert_item("letter.gamma", "γ")
    b.insert_item("letter.delta", "δ")
    b.insert_item("letter.espilon", "ε")

    print(b.tuples)


# Unit tests here could be a convenient way of testing the library code.
# But, they don't have to be here. We can keep them separate in the tests
# module.
class TestBoxModule(unittest.TestCase):
    def test_insert_items_int(self):
        goods = [
            ("yjygca.m2jf1e.qiaja5", 7),
            ("k63gcm.g0vywh.f1y2ex", 13),
            ("beba9t.ru9kns.39fcon", 107),
        ]
        bads = [
            ("3dd54u.a6iys9.5tcpc2", 61),
            ("81198a.8eoom0.jr84if", 19),
            ("9j2lqa.058tun.3mooy7", 89),
        ]

        b = Box()
        #
        # Negative test
        #
        for (key, value) in bads:
            # Validate that expected assertion is raised on error.
            with self.assertRaises(BoxKeyValidationError):
                b.insert_item(key, value)
        # All keys in bads should be absent from our box. If any are found
        # this test is a failure.
        for (key, value) in bads:
            with self.assertRaises(BoxUnknownKeyError):
                b.get(key)
        #
        # Positive test
        #
        for (key, value) in goods:
            b.insert_item(key, value)
        # All keys in goods should be in our box. If any are not found
        # this test is a failure.
        for (key, value) in goods:
            self.assertIsNotNone(b.get(key))
            self.assertEqual(b.get(key), value)

    def test_insert_item_string(self):
        goods = (
            ("yjygca.m2jf1e.qiaja5", "7"),
            ("k63gcm.g0vywh.f1y2ex", "13"),
            ("beba9t.ru9kns.39fcon", "107"),
        )
        bads = (
            ("3dd54u.a6iys9.5tcpc2", "61"),
            ("81198a.8eoom0.jr84if", "19"),
            ("9j2lqa.058tun.3mooy7", "89"),
        )

        b = Box()
        #
        # Negative test
        #
        for (key, value) in bads:
            # Validate that expected assertion is raised on error.
            with self.assertRaises(BoxKeyValidationError):
                b.insert_item(key, value)
        # All keys in bads should be absent from our box. If any are found
        # this test is a failure.
        for (key, value) in bads:
            with self.assertRaises(BoxUnknownKeyError):
                b.get(key)
        #
        # Positive test
        #
        for (key, value) in goods:
            b.insert_item(key, value)
        # All keys in goods should be in our box. If any are not found
        # this test is a failure.
        for (key, value) in goods:
            self.assertIsNotNone(b.get(key))
            self.assertEqual(b.get(key), value)

    def test_update_item(self):
        bads = ("521", 521, True, None)
        b = Box()
        # We should get a BoxKeyError exception on any update of non-existent
        # keys.
        for v in bads:
            with self.assertRaises(BoxKeyError):
                b.update_item("beba9t.ru9kns.39fcon", v)

    def test_remove_item(self):
        items = (
            ("yjygca.m2jf1e.qiaja5", "7"),
            ("k63gcm.g0vywh.f1y2ex", "13"),
            ("beba9t.ru9kns.39fcon", "107"),
        )
        b = Box()
        for key, value in items:
            b.insert_item(key, value)
            self.assertIn(key, b)

        for key, value in items:
            b.remove_item(key)
            self.assertNotIn(key, b)


if __name__ == "pypkgexp1.cli":
    print("🚀 Launched from REPL, command line or 'python -m unittest ...'")

# This will not run when called from the command line because setuptools
# installs a custom script which makes sure that the main function is called
# effectively like: pypkgexp1.cli.main_func
if __name__ == "__main__":
    unittest.main()
