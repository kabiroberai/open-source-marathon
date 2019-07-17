from urllib.parse import urljoin
from html.parser import HTMLParser


class _Parser(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.url = url

        self.links = []

    def error(self, message):
        print(f"Error: { message }")

    def handle_link(self, link):
        parsed_link = urljoin(self.url, link)
        self.links.append(parsed_link)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    self.handle_link(value)

    def handle_data(self, data):
        pass


# currently only returns links
# additional features will be added in a later task
def parse(text, url):
    parser = _Parser(url)
    parser.feed(text)
    return parser.links
