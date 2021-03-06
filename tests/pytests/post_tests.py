import unittest
import requests
import simplejson
import lxml

from lxml import html
from urlparse import urlparse
from yayclient import YayClient, OldYayClient

class TestPostFunction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.opts = dict(
            url = 'http://yayhooray.dev/'
        )

        user = YayClient.register(cls.opts, 'yay2tester', 'a@a.com', 'a', 'a')
        thread = YayClient.post_thread(cls.opts, user.cookies, 2, "Test", "Test")

        cls.cookies = user.cookies
        cls.thread = urlparse(thread.url).path[1:]

    def post_reply(self, content):
        r = YayClient.post_reply(self.opts, self.cookies, self.thread, content)
        tree = lxml.html.fromstring(r.content)
        return tree.cssselect(".comment")[-1].cssselect(".content")[0]


    def test_basic(self):
        r = YayClient.post_reply(self.opts, self.cookies, self.thread, "new post")
        self.assertEqual(r.status_code, 200)

    def test_script(self):
        reply = self.post_reply("<script>alert(\"hello\");</script>")
        self.assertFalse(reply.cssselect("script"))


    def test_js_href(self):
        reply = self.post_reply("<a href=\"Javascript:alert('hello');\">hello</a>")
        self.assertEqual(None, reply.cssselect("a")[0].get("href"))


if __name__ == '__main__':
    unittest.main()
