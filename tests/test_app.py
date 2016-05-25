import unittest

from StringIO import StringIO

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

import testapp


class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = Client(testapp.app, BaseResponse)

    def test_hello_get(self):
        r = self.client.get('/testapp/hello/?who=Tester')
        self.assertEqual(r.data, '"Hello Tester"')

    def test_hello_urlencoded_get(self):
        r = self.client.get('/testapp/hello/?who=Arthur%20Dent')
        self.assertEqual(r.data, '"Hello Arthur Dent"')

    def test_hello_post(self):
        r = self.client.post('/testapp/hello/', data=dict(who='Tester'))
        self.assertEqual(r.data, '"Hello Tester"')

    def test_hello_post_json(self):
        r = self.client.post(
            '/testapp/hello/',
            data='{"who": "Tester"}',
            content_type='application/json')
        self.assertEqual(r.data, '"Hello Tester"')

    def test_multiply_get(self):
        r = self.client.get('/testapp/multiply/?x=6&y=7')
        self.assertEqual(r.data, '42')

    def test_multiply_str_get(self):
        r = self.client.get('/testapp/multiply/?x=a&y=7')
        self.assertEqual(r.data, '"aaaaaaa"')

    def test_multiply_post(self):
        r = self.client.post('/testapp/multiply/', data=dict(x=6, y=7))
        self.assertEqual(r.data, '42')

    def test_multiply_post_json(self):
        r = self.client.post(
            '/testapp/multiply/',
            data='{"x": 6, "y": 7}',
            content_type='application/json')
        self.assertEqual(r.data, '42')

    def test_upload_post(self):
        r = self.client.post(
            '/testapp/upload/',
            data={'upload': (StringIO('some file contents'), 'test.txt')})
        self.assertEqual(r.data, '"some file contents"')

    def test_post_only_post(self):
        r = self.client.post('/testapp/post_only/')
        self.assertEqual(r.data, 'true')

    def test_post_only_get(self):
        r = self.client.get('/testapp/post_only/')
        self.assertEqual(r.status, '405 METHOD NOT ALLOWED')

    def test_not_post_only_get(self):
        r = self.client.get('/testapp/not_post_only/')
        self.assertEqual(r.data, 'true')

    def test_request_arg1(self):
        r = self.client.get('/testapp/my_ip1/', environ_overrides={'REMOTE_ADDR': '127.0.0.1'})
        self.assertEqual(r.data, '"127.0.0.1"')

    def test_request_arg2(self):
        r = self.client.get('/testapp/my_ip2/', environ_overrides={'REMOTE_ADDR': '127.0.0.1'})
        self.assertEqual(r.data, '"127.0.0.1"')

    def test_request_arg3(self):
        r = self.client.get('/testapp/my_ip3/', environ_overrides={'REMOTE_ADDR': '127.0.0.1'})
        self.assertEqual(r.data, '"127.0.0.1"')

    def test_current_user(self):
        r = self.client.get('/testapp/current_user/')
        self.assertEqual(r.data, '"arthurd42"')

    def test_get_cookie(self):
        r = self.client.get('/testapp/session_id/')
        self.assertEqual(r.data, 'null')
        r = self.client.get('/testapp/start_session/')
        r = self.client.get('/testapp/session_id/')
        self.assertEqual(r.data, '"42"')

    def test_delete_cookie(self):
        r = self.client.get('/testapp/start_session/')
        r = self.client.get('/testapp/session_id/')
        self.assertEqual(r.data, '"42"')
        r = self.client.get('/testapp/end_session/')
        r = self.client.get('/testapp/session_id/')
        self.assertEqual(r.data, 'null')

    def test_headers(self):
        r = self.client.get('/testapp/session_id2/', headers={'session_id': '42'})
        self.assertEqual(r.data, '"42"')

    def test_stream(self):
        r = self.client.get('/testapp/streamer/?n=1')
        self.assertEqual(r.headers['content-type'], 'text/event-stream')


if __name__ == '__main__':
    unittest.main()
