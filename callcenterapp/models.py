# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class CallDetail(models.Model):
    """
    Model to store the phone call metadata.
    """
    event_timestamp = models.DateTimeField()
    queue_enter_time = models.DateTimeField()
    caller_id_num = models.CharField(max_length=30)
    caller_id_name = models.CharField(max_length=100)
    queue_name = models.CharField(max_length=30)
    queue_id = models.UUIDField(max_length=256)
    session_id = models.UUIDField(max_length=256)
    event_name = models.CharField(max_length=30)
    recipient_id = models.UUIDField(max_length=30)
    recipient_name = models.CharField(max_length=30)
    total_wait_time = models.IntegerField()

    def __str__(self):
        return str(self.session_id)


class PhoneCall(models.Model):
    """
    Model to store the phone call data.
    """
    action = models.CharField(max_length=30)
    name = models.CharField(max_length=30, unique=True)
    data = models.OneToOneField(CallDetail, on_delete=models.CASCADE)

    def get_total_wait_time(self):
        return int(self.data.total_wait_time)

    def get_queue_name(self):
        return self.data.queue_name

    def get_caller_id_name(self):
        return self.data.caller_id_name

    def get_recipient_id(self):
        return self.data.recipient_id

    def __str__(self):
        return self.name


class JiraTriggerConfiguration(models.Model):
    """
    Table to store configurations which can trigger the JIRA creation task.
    """
    total_wait_time = models.IntegerField()
    queue_name = models.CharField(max_length=30)
    caller_id_name = models.CharField(max_length=100)
    recipient_id = models.UUIDField(max_length=30)

    def __str__(self):
        data = self.__dict__.copy()
        data.pop('_state', None)

        return data.__str__()

    def check_if_jira_threshold_met(self, phone_call_instance):
        return phone_call_instance.get_total_wait_time() > self.total_wait_time or \
               phone_call_instance.get_queue_name() == self.queue_name or \
               phone_call_instance.get_caller_id_name() == self.caller_id_name or \
               phone_call_instance.get_recipient_id() == self.recipient_id
