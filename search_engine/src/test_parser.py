from django.test import TestCase
from .management.commands.scraper.parser import parse


class ParserTestCase(TestCase):
    def parse(self, text):
        return parse(text, 'https://example.com')

    def test_title(self):
        data = self.parse('<title>Hello, world!</title>')
        self.assertEqual(data.title, 'Hello, world!')

    def test_robots(self):
        data = self.parse('<html></html>')
        self.assertTrue(data.should_follow)
        self.assertTrue(data.should_index)
        data = self.parse('<meta name="robots" content="nofollow">')
        self.assertFalse(data.should_follow)
        self.assertTrue(data.should_index)
        data = self.parse('<meta name="robots" content="noindex">')
        self.assertTrue(data.should_follow)
        self.assertFalse(data.should_index)
        data = self.parse('<meta name="robots" content="noindex, nofollow">')
        self.assertFalse(data.should_follow)
        self.assertFalse(data.should_index)
        data = self.parse('<meta name="robots" content="noindex,nofollow">')
        self.assertFalse(data.should_follow)
        self.assertFalse(data.should_index)

    def test_open_graph(self):
        data = self.parse('<meta property="og:title" content="Hello">')
        self.assertEqual(data.open_graph['title'], 'Hello')
