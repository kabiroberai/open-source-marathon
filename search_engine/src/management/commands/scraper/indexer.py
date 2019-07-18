from src.models import Entry, SearchTerm, Lemma, Synset
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
    entry = Entry(
        url=graph[-1],
        shouldFollow=parsed.should_follow,
        title=parsed.title,
        text=parsed.text,
        open_graph=dumps(parsed.open_graph)
    )
    entry.save()

    words = wordpunct_tokenize(parsed.text)
    tagged = pos_tag(words)
    alpha_words = [(w.lower(), tag_to_pos(t)) for (w, t) in tagged if w.isalpha()]
    for (word, pos) in alpha_words:
        term = get_or_create_term(word, pos)
        term.entries.add(entry)
