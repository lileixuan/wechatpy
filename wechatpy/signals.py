# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from blinker import signal


# WeChat Client access token granted
access_token_granted = signal('access-token-granted')
# WeChat Client access token expired
access_token_expired = signal('access-token-expired')
