from src.models import Entry, SearchTerm
from json import dumps


def index(parsed, graph):
    print(" > ".join(graph))
    entry = Entry(
        url=graph[-1],
        shouldFollow=parsed.should_follow,
        title=parsed.title,
        text=parsed.text,
        open_graph=dumps(parsed.open_graph)
    )
    entry.save()
    # at present we just store the raw word, but in a later task we'll strip punctuation etc
    # and also store concepts
    word_set = set(filter(lambda w: w.strip() != '', parsed.text.split(' ')))
    for word in word_set:
        try:
            term = SearchTerm.objects.get(pk=word)
        except SearchTerm.DoesNotExist:
            term = SearchTerm(term=word)
            term.save()
        term.entries.add(entry)

