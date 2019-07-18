# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Entry(models.Model):
    url = models.TextField(primary_key=True)
    shouldFollow = models.BooleanField()
    title = models.TextField()
    text = models.TextField()
    open_graph = models.TextField()  # as json

    def __str__(self):
        return self.url


# inverted index
class SearchTerm(models.Model):
    term = models.CharField(max_length=100, primary_key=True)
    entries = models.ManyToManyField(Entry)

    def __str__(self):
        return self.term
