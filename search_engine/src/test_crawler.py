from django.test import TestCase
from .management.commands.scraper.crawler import *
import json


class CrawlerTestCase(TestCase):
    def test_valid_request(self):
        response = make_request('https://postman-echo.com/headers')
        self.assertIsNotNone(response)
        with response:
            val = response.read()
            self.assertIsNotNone(val)
            decoded = val.decode('utf-8')
            self.assertIsNotNone(decoded)
            self.assertEqual(json.loads(decoded)['headers']['user-agent'], 'Mozilla/5.0 (compatible; QuarryBot/1.0)')

    def test_duplicate_urls(self):
        self.assertTrue(should_crawl(['https://wikipedia.org', 'https://wikimedia.org']))
        self.assertFalse(should_crawl(['https://wikipedia.org', 'https://wikimedia.org', 'https://wikipedia.org']))

    def test_unsupported_schemes(self):
        self.assertFalse(should_crawl(['mailto:me@example.com']))

    def test_same_host_limit(self):
        self.assertTrue(should_crawl(['https://wikipedia.org/a', 'https://wikipedia.org/b']))
        self.assertFalse(should_crawl(['https://wikipedia.org/a', 'https://wikipedia.org/b', 'https://wikipedia.org/c']))

    def test_parse_robots(self):
        self.assertFalse(should_crawl(['https://www.google.com/groups']))
