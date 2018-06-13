# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')
        print(asset_data)
        return HttpResponse(u'成功收到数据！')
    else:
        return HttpResponse(u'只能使用 POST 方法')
