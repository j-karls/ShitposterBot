import unittest

#class TestDatabase(unittest.TestCase):
# setup and teardown wth custom database path


class TestJson(unittest.TestCase):
    # It's a requirement that all test function names start with 'test'

    def test_getjson_validwebsite_success(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
