from igolf import *
from marshalI import *
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re


class golfweb:

    def get_html_parser(self, url):
        o = urlparse(url)
        if o.hostname == "v2anegasaki.igolfshaper.com":
            return igolf(url)
        if re.match("marshal-i.com", o.hostname):
            return marshalI(url)

        raise ValueError("Unhandled url")

    def get_scores(self, url):
        x = self.get_html_parser(url)
        try:
            data = x.get_scores()
            return data
        except Exception as e:
            print(e)
            # raise ValueError("Parse failed")
            raise ValueError(str(e))


if __name__ == "__main__":
    x = golfweb()
    r = x.get_scores(
        # 'https://marshal-i.com/ops/score/oakvillage_20231031_7bf14538'
        'https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre#/landscape-a'
    )
    print(r)
