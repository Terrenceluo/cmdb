# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig


class AssetsConfig(AppConfig):
    name = 'assets'
    verbose_name = _('Assets')
