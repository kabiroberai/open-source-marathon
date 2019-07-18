from src.models import Entry, Link, SearchTerm, Lemma, Synset
from json import dumps
from nltk import wordpunct_tokenize, pos_tag, WordNetLemmatizer
from nltk.corpus import wordnet as wn


def tag_to_pos(tag):
    return {
        'J': wn.ADJ,
        'N': wn.NOUN,
        'V': wn.VERB,
        'R': wn.ADV,
    }.get(tag.upper()[0], wn.NOUN)


lemmatizer = WordNetLemmatizer()


# we shouldn't always save syn, because that could lead to infinite recursion
def get_or_create_term(word, pos):
    term, _ = SearchTerm.objects.get_or_create(term=word, pos=pos)

    wn_lemma_word = lemmatizer.lemmatize(word, pos)
    wn_lemmas = wn.lemmas(wn_lemma_word, pos)
    for wn_lemma in wn_lemmas:
        synset, _ = Synset.objects.get_or_create(name=wn_lemma.synset().name())
        lemma, _ = Lemma.objects.get_or_create(name=wn_lemma.name(), defaults={'synset': synset})
        term.lemmas.add(lemma)

    return term


def index(parsed, graph):
    print(" > ".join(graph))

    link, _ = Link.objects.get_or_create(url=graph[-1])
    if len(graph) == 1:
        link.is_top_level = True
        link.save()

    entry, _ = Entry.objects.update_or_create(
        link=link,
        title=parsed.title,
        text=parsed.text,
        open_graph=dumps(parsed.open_graph)
    )
    for url in parsed.links:
        url_link, _ = Link.objects.get_or_create(url=url)
        url_link.referrers.add(link)

    words = wordpunct_tokenize(f"{parsed.title}\n{parsed.text}")
    tagged = pos_tag(words)
    alpha_words = [(w.lower(), tag_to_pos(t)) for (w, t) in tagged if w.isalpha()]
    for (word, pos) in alpha_words:
        term = get_or_create_term(word, pos)
        term.entries.add(entry)
