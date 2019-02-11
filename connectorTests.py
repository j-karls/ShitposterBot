import unittest

import connector
import requests

import loader


class TestJson(unittest.TestCase):
    # It's a requirement that all test function names start with 'test'

    def test_getjson_validwebsite_success(self):
        self.assertEqual('foo'.upper(), 'FOO')

#    def test_getjson_validwebsite_successasfasf(self):
#        r = requests.get(f'https://www.reddit.com/r/pics.json', headers={'User-agent': 'shitposterBot 0.1'}).json()
#        el = r["data"]["children"][0]
#        try:
#            print(el["data"]["url"])
#        except KeyError:
#            print("No url")
#        self.assertEqual('foo'.upper(), 'FOO')

    def test_loader_valid_success(self):
        links = loader.get_reddit_links("pics", 5, "hourly", True)
        [print(x) for x in links]
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
