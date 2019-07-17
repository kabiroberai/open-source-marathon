class ParsedData:
    def __init__(self):
        self.links = []
        self.should_index = True
        self.should_follow = True
        self.title = ''
        self.text = ''
        self.word_set = set()
        self.open_graph = {}

    def __str__(self):
        return f"""
Title: { self.title }
Should Index: { self.should_index }
Should Follow: { self.should_follow }
Open Graph Metadata: { self.open_graph }
Words: { self.word_set }
Links: { self.links }
"""
