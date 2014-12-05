
import HTMLParser
class ClearHTMLTag(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self,d):
        self.fed.append(d)

    def get_data(self):
        return "".join(self.fed)

def clear_tags(html):
    s = ClearHTMLTag()
    s.feed(html)
    return s.get_data()

if __name__ == "__main__":
    html = "<td colspan='1'>aaaa</td>"
    print clear_tags(html)
