from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from .parser import parse
from datetime import datetime


MAX_SAME_HOST_COUNT = 3


# order the links
def order_links(links, graph):
    url = graph[-1]
    links.sort(key=lambda link: urlparse(link).hostname == urlparse(url).hostname)


# determines whether this is a "dead end"
def is_leaf(graph):
    # if we've seen this link before, then it's definitely a dead end
    if graph[-1] in graph[:-1]:
        return True

    parsed = urlparse(graph[-1])

    # only parse http and https
    if parsed.scheme not in ['http', 'https']:
        return True

    if len(graph) >= MAX_SAME_HOST_COUNT:
        # if the last MAX_SAME_HOST_COUNT elements were of the same host, then exit
        host = parsed.hostname
        recent = graph[-MAX_SAME_HOST_COUNT:]
        has_recent_non_same_host = False
        for link in recent:
            if urlparse(link).hostname != host:
                has_recent_non_same_host = True
                break
        if not has_recent_non_same_host:
            return True

    return False


def handle_response(response, graph):
    data = response.read()
    if data is None:
        return []
    try:
        text = data.decode(response.headers.get_content_charset() or "utf-8")
    except UnicodeDecodeError:
        return []
    links = parse(text, graph[-1])
    order_links(links, graph)

    print(f"Date: { datetime.now() }")

    # Note: We could print `text` but we don't since that would just spam the console

    return links


def _crawl(graph):
    if is_leaf(graph):
        return

    print(" > ".join(graph))
    print()

    url = graph[-1]

    try:
        response = urlopen(url)
    except HTTPError as e:
        print(e)
        return

    with response:
        links = handle_response(response, graph)
        for link in links:
            if link == url:
                continue
            _crawl(graph + [link])


def crawl(url):
    _crawl([url])
