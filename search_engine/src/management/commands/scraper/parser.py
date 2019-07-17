from urllib.parse import urljoin
from html.parser import HTMLParser
from .ParsedData import ParsedData


class _Parser(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.data = ParsedData()

    def error(self, message):
        print(f"Error: { message }")

    def handle_link(self, link):
        parsed_link = urljoin(self.url, link)
        self.data.links.append(parsed_link)

    def parse_meta_robots(self, value):
        index = True
        follow = True
        elements = value.split(",")
        for element in elements:
            key = element.strip().upper()
            if key == 'NOINDEX':
                index = False
            elif key == 'INDEX':
                index = True
            elif key == 'NOFOLLOW':
                follow = False
            elif key == 'FOLLOW':
                follow = True
        return index, follow

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            for (key, value) in attrs:
                if key == 'robots':
                    (self.data.should_index, self.data.should_follow) = self.parse_meta_robots(value)

        if tag == 'a':
            should_follow = True
            link = None
            for (key, value) in attrs:
                if key == 'href':
                    link = value
                elif key == 'rel' and value == 'nofollow':
                    should_follow = False
            if should_follow and link is not None:
                self.handle_link(link)

    def handle_data(self, data):
        pass


# currently only returns links
# additional features will be added in a later task
def parse(text, url):
    parser = _Parser(url)
    parser.feed(text)
    return parser.data
