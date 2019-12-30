import unittest

from pypkgexp1.lib.box import Box, BoxKeyError, BoxKeyValidationError

# Unit tests here could be a convenient way of testing the library code.
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
            self.assertIsNone(b.get(key))
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
            self.assertIsNone(b.get(key))
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


if __name__ == "__main__":
    unittest.main()
