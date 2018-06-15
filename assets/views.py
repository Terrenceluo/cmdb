# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from assets import models, asset_handler


@csrf_exempt
def report(request):
    """
    通过csrf_exempt装饰器，跳过Django的csrf安全机制，让post的数据能被接收，但这又会带来新的安全问题。
    可以在客户端，使用自定义的认证token，进行身份验证。这部分工作，请根据实际情况，自己进行。
    :param request:
    :return:
    """
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        # 各种数据检查，请自行添加和完善！
        if not data:
            return HttpResponse(_('Data not found'))
        if not issubclass(dict, type(data)):
            return HttpResponse(_('Data must be dict'))
        # 是否携带了关键的sn号
        sn = data.get('sn', None)
        if sn:
            # 进入审批流程
            # 首先判断是否在上线资产中存在该sn
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                # 进入已上线资产的数据更新流程
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse(_('Asset data has updated'))
            else:  # 如果已上线资产中没有，那么说明是未批准资产，进入新资产待审批区，更新或者创建资产。
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse(_('Serial number not found, please check data'))
    else:
        return HttpResponse(_('Only post method'))


def index(request):
    assets = models.Asset.objects.all()
    return render(request, 'assets/index.html', locals())


def dashboard(request):
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breakdown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()
    up_rate = round(float(upline) / float(total) * 100)
    o_rate = round(float(offline) / float(total) * 100)
    un_rate = round(float(unknown) / float(total) * 100)
    bd_rate = round(float(breakdown) / float(total) * 100)
    bu_rate = round(float(backup) / float(total) * 100)
    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    storagedevice_number = models.StorageDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()

    return render(request, 'assets/dashboard.html', locals())


def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """
    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'assets/detail.html', locals())
