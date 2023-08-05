# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from email.utils import formatdate

import time


class SetCookieView(BrowserView):
    def __call__(self):
        expiration_seconds = time.time() + ((24 * 60 * 60) * 30 * 12 * 10)  # 10 years
        expires = formatdate(expiration_seconds, usegmt=True)
        self.request.response.setCookie(
            "hide-dsgvo-banner", "true", path="/", expires=expires
        )
        self.request.response.setStatus(201)
