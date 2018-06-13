# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Asset(models.Model):
    """    所有资产的共有数据表    """
    asset_type_choice = (
        ('server', _('Server')),  # 服务器
        ('networkdevice', _('Network device')),  # 网络设备
        ('storagedevice', _('Storage device')),  # 存储设备
        ('securitydevice', _('Security device')),  # 安全设备
        ('software', u'软件资产'),
    )

    asset_status = (
        (0, _('Online')),  # 在线
        (1, _('Offline')),  # 下线
        (2, _('Unknown')),  # 未知
        (3, _('Breakdown')),  # 故障
        (4, _('Spare')),  # 备用
    )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server',
                                  verbose_name=_('Asset type'))  # 资产类型
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Asset name'))  # 资产名称
    sn = models.CharField(max_length=128, unique=True, verbose_name=_('Asset serial number'))  # 资产序列号
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name=_('Business unit'))  # 所属业务线
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name=_('Equipment status'))  # 设备状态

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name=_('Manufacturer'))  # 制造商
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('Manage IP'))  # 管理IP
    tags = models.ManyToManyField('Tag', blank=True, verbose_name=_('Tag'))  # 标签
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name=_('Asset admin'), related_name='admin')  # 资产管理员
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name=_('IDC'))  # 所在机房
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name=_('Contract'))  # 合同

    purchase_day = models.DateField(null=True, blank=True, verbose_name=_('Purchase day'))  # 购买日期
    expire_day = models.DateField(null=True, blank=True, verbose_name=_('Expire day'))  # 过保日期
    price = models.FloatField(null=True, blank=True, verbose_name=_('Price'))  # 价格

    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name=_('Approver'),
                                    related_name='approved_by')  # 批准人

    memo = models.TextField(null=True, blank=True, verbose_name=_('Memo'))  # 备注
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Approval date'))  # 批准日期
    m_time = models.DateTimeField(auto_now=True, verbose_name=_('Modify date'))  # 更新日期

    def __unicode__(self):
        return '<%s>  %s' % (self.get_asset_type_display(), self.name)

    class Meta:
        verbose_name = _('Asset summary statement')  # 资产总表
        verbose_name_plural = _('Asset summary statement')  # 资产总表
        ordering = ['-c_time']


class Server(models.Model):
    """    服务器设备    """
    sub_asset_type_choice = (
        (0, _('PC Server')),  # PC服务器
        (1, _('Blade')),  # 刀片机
        (2, _('Minicomputer')),  # 小型机
    )

    created_by_choice = (
        ('auto', _('Automatically add')),  # 自动添加
        ('manual', _('Manual input')),  # 手工录入
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0,
                                              verbose_name=_('Server type'))  # 服务器类型
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto',
                                  verbose_name=_('Add mode'))  # 添加方式
    # 虚拟机专用字段
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True,
                                  verbose_name=_('Host'))  # 宿主机
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Server model'))  # 服务器型号
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('Raid type'))  # Raid类型

    os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('OS type'))  # 操作系统类型
    os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('OS distribution'))  # 发行版本
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('OS release'))  # 操作系统版本

    def __unicode__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = _('Server')  # 服务器
        verbose_name_plural = _('Server')  # 服务器


class SecurityDevice(models.Model):
    """    安全设备    """
    sub_asset_type_choice = (
        (0, _('Fire wall')),  # 防火墙
        (1, _('Intrusion detection device')),  # 入侵检测设备
        (2, _('Internet gateway')),  # 互联网网关
        (4, _('SSA')),  # 运维审计系统
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name=u'安全设备类型')

    def __unicode__(self):
        return self.asset.name + '--' + self.get_sub_asset_type_display() + ' id:%s' % self.id

    class Meta:
        verbose_name = u'安全设备'
        verbose_name_plural = u'安全设备'


class StorageDevice(models.Model):
    """    存储设备    """
    sub_asset_type_choice = (
        (0, u'磁盘阵列'),
        (1, u'网络存储器'),
        (2, u'磁带库'),
        (4, u'磁带机'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name=u'存储设备类型')

    def __unicode__(self):
        return self.asset.name + '--' + self.get_sub_asset_type_display() + ' id:%s' % self.id

    class Meta:
        verbose_name = u'存储设备'
        verbose_name_plural = u'存储设备'


class NetworkDevice(models.Model):
    """    网络设备    """
    sub_asset_type_choice = (
        (0, u'路由器'),
        (1, u'交换机'),
        (2, u'负载均衡'),
        (4, u'VPN设备'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name=u'网络设备类型')

    # 局域网 IP
    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='VLanIP')
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name=u'内网IP')

    model = models.CharField(max_length=128, null=True, blank=True, verbose_name=u'网络设备型号')
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'设备固件版本')
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name=u'端口个数')
    device_detail = models.TextField(null=True, blank=True, verbose_name=u'详细配置')

    def __unicode__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = u'网络设备'
        verbose_name_plural = u'网络设备'


class Software(models.Model):
    """    只保存付费购买的软件    """
    sub_asset_type_choice = (
        (0, u'操作系统'),
        (1, u'办公\开发软件'),
        (2, u'业务软件'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name=u'软件类型')
    license_num = models.IntegerField(default=1, verbose_name=u'授权数量')
    version = models.CharField(max_length=64, unique=True, help_text=u'例如: CentOS release 6.7 (Final)',
                               verbose_name=u'软件/系统版本')

    def __unicode__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = u'软件/系统'
        verbose_name_plural = u'软件/系统'


class IDC(models.Model):
    """    机房    """
    name = models.CharField(max_length=64, unique=True, verbose_name=u'机房名称')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'备注')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'机房'
        verbose_name_plural = u'机房'


class Manufacturer(models.Model):
    """    厂商    """
    name = models.CharField(u'厂商名称', max_length=64, unique=True)
    telephone = models.CharField(u'支持电话', max_length=30, blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'厂商'
        verbose_name_plural = u'厂商'


class BusinessUnit(models.Model):
    """    业务线    """
    parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level')
    name = models.CharField(u'业务线', max_length=64, unique=True)
    memo = models.CharField(u'备注', max_length=64, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'业务线'
        verbose_name_plural = u'业务线'


class Contract(models.Model):
    """    合同    """
    sn = models.CharField(u'合同号', max_length=128, unique=True)
    name = models.CharField(u'合同名称', max_length=64)
    memo = models.TextField(u'备注', blank=True, null=True)
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同详细', blank=True, null=True)
    start_day = models.DateField(u'开始日期', blank=True, null=True)
    end_day = models.DateField(u'失效日期', blank=True, null=True)
    license_num = models.IntegerField(u'license数量', blank=True, null=True)
    c_day = models.DateField(u'创建日期', auto_now_add=True)
    m_day = models.DateField(u'修改日期', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'合同'
        verbose_name_plural = u'合同'


class Tag(models.Model):
    """    标签    """
    name = models.CharField(u'标签名', max_length=32, unique=True)
    c_day = models.DateField(u'创建日期', auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'


class CPU(models.Model):
    """    CPU组件    """
    asset = models.OneToOneField('Asset')  # 设备上的cpu肯定都是一样的，所以不需要建立多个cpu数据，一条就可以，因此使用一对一。
    cpu_model = models.CharField(u'CPU型号', max_length=128, blank=True, null=True)
    cpu_count = models.PositiveSmallIntegerField(u'物理CPU个数', default=1)
    cpu_core_count = models.PositiveSmallIntegerField(u'CPU核数', default=1)

    def __unicode__(self):
        return self.asset.name + ':   ' + self.cpu_model

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPU'


class RAM(models.Model):
    """    内存组件    """
    asset = models.ForeignKey('Asset')  # 只能通过外键关联Asset。否则不能同时关联服务器、网络设备等等。
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    model = models.CharField(u'内存型号', max_length=128, blank=True, null=True)
    manufacturer = models.CharField(u'内存制造商', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(GB)', blank=True, null=True)

    def __unicode__(self):
        return '%s: %s: %s: %s' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = u'内存'
        verbose_name_plural = u'内存'
        unique_together = ('asset', 'slot')  # 同一资产下的内存，根据插槽的不同，必须唯一


class Disk(models.Model):
    """    存储设备    """
    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'硬盘SN号', max_length=128)
    slot = models.CharField(u'所在插槽位', max_length=64, blank=True, null=True)
    model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
    manufacturer = models.CharField(u'磁盘制造商', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'磁盘容量(GB)', blank=True, null=True)
    interface_type = models.CharField(u'接口类型', max_length=16, choices=disk_interface_type_choice, default='unknown')

    def __unicode__(self):
        return '%s:  %s:  %s:  %sGB' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = u'硬盘'
        verbose_name_plural = u'硬盘'
        unique_together = ('asset', 'sn')


class NIC(models.Model):
    """    网卡组件    """
    asset = models.ForeignKey('Asset')  # 注意要用外键
    name = models.CharField(u'网卡名称', max_length=64, blank=True, null=True)
    model = models.CharField(u'网卡型号', max_length=128)
    mac = models.CharField(u'MAC地址', max_length=64)  # 虚拟机有可能会出现同样的mac地址
    ip_address = models.GenericIPAddressField(u'IP地址', blank=True, null=True)
    net_mask = models.CharField(u'掩码', max_length=64, blank=True, null=True)
    bonding = models.CharField(u'绑定地址', max_length=64, blank=True, null=True)

    def __unicode__(self):
        return '%s:  %s:  %s' % (self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u'网卡'
        unique_together = ('asset', 'model', 'mac')  # 资产、型号和mac必须联合唯一。防止虚拟机中的特殊情况发生错误。


class EventLog(models.Model):
    """
    日志.
    在关联对象被删除的时候，不能一并删除，需保留日志。
    因此，on_delete=models.SET_NULL
    """
    name = models.CharField(u'事件名称', max_length=128)
    event_type_choice = (
        (0, u'其它'),
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
    )
    # 当资产审批成功时有这项数据
    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)
    # 当资产审批失败时有这项数据
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choice, default=4)
    component = models.CharField(u'事件子项', max_length=256, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    # 自动更新资产数据时没有执行人
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=u'事件执行人', on_delete=models.SET_NULL)
    memo = models.TextField(u'备注', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'事件纪录'
        verbose_name_plural = u'事件纪录'


class NewAssetApprovalZone(models.Model):
    """    新资产待审批区    """
    sn = models.CharField(u'资产SN号', max_length=128, unique=True)  # 此字段必填
    asset_type_choice = (
        ('server', u'服务器'),
        ('networkdevice', u'网络设备'),
        ('storagedevice', u'存储设备'),
        ('securitydevice', u'安全设备'),
        ('IDC', u'机房'),
        ('software', u'软件资产'),
    )
    asset_type = models.CharField(choices=asset_type_choice, default='server', max_length=64, blank=True, null=True,
                                  verbose_name=u'资产类型')

    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'生产厂商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'型号')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name=u'内存大小')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField(u'物理CPU个数', blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField(u'CPU核数', blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'发行版本')
    os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'操作系统类型')
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'操作系统版本')

    data = models.TextField(u'资产数据')  # 此字段必填

    c_time = models.DateTimeField(u'汇报日期', auto_now_add=True)
    m_time = models.DateTimeField(u'数据更新日期', auto_now=True)
    approved = models.BooleanField(u'是否批准', default=False)

    def __unicode__(self):
        return self.sn

    class Meta:
        verbose_name = u'新上线待批准资产'
        verbose_name_plural = u'新上线待批准资产'
        ordering = ['-c_time']

