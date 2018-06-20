# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from help.file_upload_help import file_size_limit


def profile_photo_upload_path(self, filename):
    return '/'.join([settings.MEDIA_ROOT, self.user.username, 'profile_photo', filename])


class UserProfile(models.Model):
    """    登录用户    """
    user = models.OneToOneField(User, verbose_name=_('User'))
    profile_photo = models.ImageField(upload_to=profile_photo_upload_path, validators=[file_size_limit], null=True,
                                      blank=True, verbose_name=_('Profile photo'))
    c_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')
        ordering = ['-c_time']
