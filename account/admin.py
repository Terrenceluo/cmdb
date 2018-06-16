# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from account import models


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'c_time')
    list_filter = ('user', 'c_time')
    search_fields = ('user',)
    ordering = ('user', 'c_time')
