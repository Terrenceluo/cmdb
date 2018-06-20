#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url

from api.views import ApiEndpoint, UserList

urlpatterns = [
    # OAuth 2 endpoints:
    url(r'^hello/$', ApiEndpoint.as_view()),  # an example resource endpoint
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>\d+)/$', UserList.as_view()),
    url(r'^groups/$', UserList.as_view()),
]
