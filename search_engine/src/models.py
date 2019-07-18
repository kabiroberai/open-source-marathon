from django.db import models
from json import loads


class Entry(models.Model):
    url = models.TextField(primary_key=True)
    shouldFollow = models.BooleanField()
    title = models.TextField()
    text = models.TextField()
    open_graph = models.TextField()  # as json

    def get_open_graph(self):
        return loads(self.open_graph)

    def __str__(self):
        return self.url


# inverted index
class SearchTerm(models.Model):
    term = models.CharField(max_length=100, primary_key=True)
    entries = models.ManyToManyField(Entry)

    def __str__(self):
        return self.term
