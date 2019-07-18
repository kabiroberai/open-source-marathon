from urllib.parse import urljoin
from html.parser import HTMLParser
from .ParsedData import ParsedData


class _Parser(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.tag_stack = []
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
        self.tag_stack.append((tag, attrs))
        if tag == 'meta':
            is_robots = False
            open_graph_key = None
            content = None
            for (key, value) in attrs:
                if key == 'name' and value == 'robots':
                    is_robots = True
                elif key == 'property' and value.startswith('og:'):
                    open_graph_key = value[3:]
                elif key == 'content':
                    content = value

            if is_robots:
                (self.data.should_index, self.data.should_follow) = self.parse_meta_robots(content)

            if open_graph_key is not None:
                self.data.open_graph[open_graph_key] = content

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

    def handle_endtag(self, tag):
        self.tag_stack.pop()

    def handle_data(self, data):
        tag = self.tag_stack[-1][0] if len(self.tag_stack) > 0 else None

        if tag == 'title':
            self.data.title = data
        elif tag not in {'script', 'style'}:
            self.data.text = f"{ self.data.text } { data }".strip()


def parse(text, url):
    parser = _Parser(url)
    parser.feed(text)
    return parser.data
