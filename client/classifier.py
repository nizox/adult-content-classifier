#!/usr/bin/env python2
import re
import sys
import httplib
import urlparse
import socket
import lxml.html.clean as _clean
import mechanize

_clean.defs.safe_attrs = frozenset(['src', 'href', 'target'])
cleaner = _clean.Cleaner(style=True, remove_unknown_tags=False,
    allow_tags=['a', 'img'])
def clean(data):
    "Keep only relevant tags and remove everything else"
    return cleaner.clean_html(data)


tokenizer = re.compile(r'\S[/!?#]?[-\w]*(?:["\'=;]|/?>|:/*)?')
def tokenize(data):
    "Split the data with a HTML-aware regex"
    return [m.group() for m in tokenizer.finditer(data)]


class Classifier(object):
    "Classifier API client, mostly HTTP things"

    def __init__(self, url):
        self._part = urlparse.urlsplit(url)
        self._reset_conn()
        
    def close(self):
        if hasattr(self, "_conn"):
            self._conn.close()

    def _reset_conn(self):
        self.close()
        self._conn = httplib.HTTPConnection(self._part.netloc)

    def request(self, method, data=None):
        path = urlparse.urljoin(self._part.path, method)
        for i in range(1, 5):
            try:
                self._conn.request("POST", path, data)
                return self._conn.getresponse()
            except (socket.error, httplib.HTTPException):
                self._reset_conn()
                continue

    def classify(self, data):
        resp = self.request("classify", data)
        score = resp.read()
        resp.close()
        return float(score)

    def learn(self, data, porn=True):
        if porn:
            resp = self.request("learn?porn", data)
        else:
            resp = self.request("learn?nonporn", data)
        content = resp.read()
        resp.close()
        return content


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s url" % sys.argv[0])
        sys.exit(1)

    classifier = Classifier("http://www.ph0k.eu/~nizox/pornfilter/")
    browser = mechanize.Browser()

    try:
        response = browser.open(sys.argv[1])
        content = response.read()

        tokenized_content = tokenize(clean(content))
        tokenized_content = " ".join(tokenized_content)
        print tokenized_content

        result = classifier.classify(tokenized_content)

        print(result)
        print("Learn? (y/n)")

        question = raw_input().lower()
        if question == "y":
            print("Porn? (y/n)")
            question = raw_input().lower()
            if question == "y":
                print(c.learn(tokenized_content, True))
            else:
                print(c.learn(tokenized_content, False))
    except KeyboardInterrupt:
        pass
    finally:
        classifier.close()
