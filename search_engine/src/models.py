from django.db import models
from json import loads


class Link(models.Model):
    url = models.TextField(primary_key=True)
    is_top_level = models.BooleanField(default=False, db_index=True)
    referrers = models.ManyToManyField('self')  # sites that link to this one
    rank = models.FloatField(default=0)  # more accurate than `float`


class Entry(models.Model):
    link = models.OneToOneField(Link, on_delete=models.CASCADE, primary_key=True)  # the entry's own link
    title = models.TextField(db_index=True)
    text = models.TextField()
    open_graph = models.TextField()  # as json

    def get_open_graph(self):
        return loads(self.open_graph)

    def __str__(self):
        return self.link.url


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

