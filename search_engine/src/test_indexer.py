from django.test import TestCase
from .management.commands.scraper.indexer import index
from .management.commands.scraper.ParsedData import ParsedData
from .models import Entry, SearchTerm


class IndexerTestCase(TestCase):
    def setUp(self):
        # flush database before each test
        Entry.objects.all().delete()
        SearchTerm.objects.all().delete()

        self.data = ParsedData()
        self.data.title = 'Google'
        self.data.text = 'hello \n\n world'
        self.data.open_graph = {'image': 'https://google.com/image.png'}
        self.url = 'https://google.com'
        index(self.data, [self.url])

    def test_entry(self):
        entry = Entry.objects.get(pk=self.url)
        self.assertEqual(entry.title, self.data.title)
        self.assertEqual(entry.text, self.data.text)

    def test_search_terms_are_correct(self):
        # make sure that the white space isn't considered a term
        self.assertEqual(len(SearchTerm.objects.all()), 3)
        # ensure correct keys
        self.assertEqual(len(SearchTerm.objects.filter(term='google')), 1)
        self.assertEqual(len(SearchTerm.objects.filter(term='hello')), 1)
        self.assertEqual(len(SearchTerm.objects.filter(term='world')), 1)

    def test_search_term_relationship(self):
        search_term = SearchTerm.objects.filter(term='hello')[0]
        entries = search_term.entries.all()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].link.url, self.url)

    def test_open_graph(self):
        entry = Entry.objects.get(pk=self.url)
        self.assertEqual(entry.get_open_graph(), self.data.open_graph)
