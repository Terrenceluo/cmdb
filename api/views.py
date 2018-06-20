# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')
