# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)
