import unittest
#import connector              make a main file. Make it so I can import just connector without it running something in main.
import requests

#class TestDatabase(unittest.TestCase):
# setup and teardown wth custom database path


class TestJson(unittest.TestCase):
    # It's a requirement that all test function names start with 'test'

    def test_getjson_validwebsite_success(self):
        self.assertEqual('foo'.upper(), 'FOO')


    def test_getjson_validwebsite_successasfasf(self):
        r = requests.get(f'https://www.reddit.com/r/pics.json', headers={'User-agent': 'shitposterBot 0.1'}).json()
        print(r["data"]["children"])
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
