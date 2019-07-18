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


# a "concept"
class Synset(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


# the root of a word
class Lemma(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    synset = models.ForeignKey(Synset, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# inverted index
class SearchTerm(models.Model):
    id = models.AutoField(primary_key=True)
    term = models.CharField(max_length=100, db_index=True)
    pos = models.CharField(max_length=1)
    lemmas = models.ManyToManyField(Lemma)
    entries = models.ManyToManyField(Entry)

    def __str__(self):
        return self.term

