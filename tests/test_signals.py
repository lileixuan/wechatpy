# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import os
import unittest

from httmock import urlmatch, HTTMock, response

from wechatpy import WeChatClient
from wechatpy._compat import json


_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_FIXTURE_PATH = os.path.join(_TESTS_PATH, 'fixtures')


@urlmatch(netloc=r'(.*\.)?api\.weixin\.qq\.com$')
def wechat_api_mock(url, request):
    path = url.path.replace('/cgi-bin/', '').replace('/', '_')
    if path.startswith('_'):
        path = path[1:]
    res_file = os.path.join(_FIXTURE_PATH, '%s.json' % path)
    content = {
        'errcode': 99999,
        'errmsg': 'can not find fixture %s' % res_file,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        with open(res_file, 'rb') as f:
            content = json.loads(f.read().decode('utf-8'))
    except (IOError, ValueError) as e:
        print(e)
    return response(200, content, headers, request=request)


class WeChatSignalsTestCase(unittest.TestCase):

    app_id = '123456'
    secret = '123456'

    def setUp(self):
        self.client = WeChatClient(self.app_id, self.secret)

    def test_access_token_granted_signal(self):
        from wechatpy.signals import access_token_granted

        @access_token_granted.connect
        def _handler(sender, access_token, expires_in):
            assert isinstance(sender, WeChatClient)
            assert access_token

        with HTTMock(wechat_api_mock):
            self.client.fetch_access_token()
