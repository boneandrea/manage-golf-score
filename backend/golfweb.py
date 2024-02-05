from igolf import *
from marshalI import *
from urllib.parse import urlparse


class golfweb:

    def get_html_parser(self, url):
        o = urlparse(url)
        print(o)
        if o.hostname == "v2anegasaki.igolfshaper.com":
            return igolf()
        if o.hostname == "marshal-i.com":
            return marshalI()

        raise ValueError("Unhandled url")

    def get_scores(self, url):
        x = self.get_html_parser(url)
        print(x)
        try:
            data = x.get_scores(url)
        except Exception as e:
            print(e)
            raise ValueError("Parse failed")

        return data
