from urllib.request import urlopen, Request
from urllib.parse import urlparse, urlunparse
from urllib.error import HTTPError
from urllib.robotparser import RobotFileParser
from time import sleep
from .parser import parse
from .indexer import index


SAME_HOST_LIMIT = 3


# robots.txt cache, keyed by scheme + netloc
site_robots = {}


# order the links
def order_links(links, graph):
    url = graph[-1]
    # links.sort(key=lambda link: urlparse(link).hostname == urlparse(url).hostname)


def parse_robots(parsed_url):
    url = urlunparse(parsed_url._replace(path='/robots.txt', params='', query='', fragment=''))
    if url in site_robots:
        return site_robots[url]
    rp = RobotFileParser(url=url)
    rp.read()
    rp.modified()
    site_robots[url] = rp
    return rp


def should_crawl(graph):
    url = graph[-1]

    # if we've seen this link before, then don't re-crawl
    if url in graph[:-1]:
        return False

    parsed = urlparse(url)

    # only parse http and https
    if parsed.scheme not in {'http', 'https'}:
        return False

    if len(graph) >= SAME_HOST_LIMIT:
        # if the last MAX_SAME_HOST_COUNT elements were of the same host, then exit.
        # this should allow the bot to circumvent DOS prevention
        host = parsed.hostname
        recent = graph[-SAME_HOST_LIMIT:]
        has_recent_non_same_host = False
        for link in recent:
            if urlparse(link).hostname != host:
                has_recent_non_same_host = True
                break
        if not has_recent_non_same_host:
            return False

    robots = parse_robots(parsed)

    if robots is not None:
        # obey robots.txt's allow and disallow rules
        if not robots.can_fetch('googlebot', url):
            return False
        # further DOS-prevention mitigation
        try:
            crawl_delay = robots.crawl_delay('googlebot')
        except AttributeError:
            # this appears to be a bug in urllib
            crawl_delay = None
        try:
            request_rate = robots.request_rate('googlebot')
        except AttributeError:
            request_rate = None
        sleep_time = None
        if crawl_delay is not None:
            sleep_time = crawl_delay
        elif request_rate is not None:
            sleep_time = request_rate.seconds / request_rate.requests
        if sleep_time is not None:
            print(f"sleeping for { sleep_time } sec")
            sleep(crawl_delay)

    return True


def handle_response(response, graph):
    robots_tag = response.info()['x-robots-tag']
    if robots_tag == 'noindex':
        return

    data = response.read()
    if data is None:
        return

    try:
        text = data.decode(response.headers.get_content_charset() or "utf-8")
    except UnicodeDecodeError:
        return

    parsed = parse(text, graph[-1])
    if not parsed.should_index:
        return

    order_links(parsed.links, graph)
    index(parsed, graph)
    if parsed.should_follow:
        for link in parsed.links:
            _crawl(graph + [link])


def _crawl(graph):
    if not should_crawl(graph):
        return

    response = make_request(graph[-1])
    if response is None:
        return

    with response:
        handle_response(response, graph)


def crawl(url):
    _crawl([url])


def make_request(url):
    request = Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; QuarryBot/1.0)'
        }
    )
    try:
        response = urlopen(request)
    except HTTPError as e:
        print(e)
        return

    return response
