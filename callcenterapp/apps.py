# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CallcenterappConfig(AppConfig):
    name = 'callcenterapp'

    def ready(self):
        from callcenterapp import signals
        s = signals
