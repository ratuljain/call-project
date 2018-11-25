# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from callcenterapp.models import CallDetail, PhoneCall, JiraTriggerConfiguration


class CallDetailsAdmin(admin.ModelAdmin):
    pass


class PhoneCallAdmin(admin.ModelAdmin):
    pass


class JiraTriggerConfigurationAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(CallDetail, CallDetailsAdmin)
admin.site.register(PhoneCall, PhoneCallAdmin)
admin.site.register(JiraTriggerConfiguration, JiraTriggerConfigurationAdmin)
