import os

from constance import config
from django.db.models.signals import post_save
from django.dispatch import receiver

from callcenterapp.jira_service import create_issue
from callcenterapp.models import PhoneCall, JiraTriggerConfiguration


@receiver(post_save, sender=PhoneCall, dispatch_uid='signals.signal_handler_post_save_user')
def signal_handler_post_save_user(sender, instance, created, **kwargs):
    """
    Method that creates a task on JIRA if certain conditions are met.
    """
    if check_if_configuration_exists(instance):
        jira_handler(instance)


def jira_handler(instance):
    """
    Method that creates a task on JIRA if certain conditions are met.

    :param instance: PhoneCall instance
    :return: None
    """
    summary = config.SUMMARY_STRING.format("testing stuff yay!")
    description = config.DESCRIPTION_STRING.format(instance.get_queue_name(), instance.get_recipient_id())

    create_issue(server_base_url='http://localhost:8080',
                 username=os.getenv('JIRA_USERNAME', 'test'),
                 password=os.getenv('JIRA_PASSWORD', 'test'),
                 project_key='test',
                 summary=summary,
                 description=description,
                 issue_type_name='Bug')


def check_if_configuration_exists(phone_call_instance):
    """
    Checks if any given threshold is met in the phone call against
    all the configurations in the JiraTriggerConfiguration model.

    :param phone_call_instance: the model instance of the phone call
    :return: boolean value
    """
    for config in JiraTriggerConfiguration.objects.all():
        if config.check_if_jira_threshold_met(phone_call_instance):
            return True

    return False
