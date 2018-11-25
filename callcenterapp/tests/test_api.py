import mock
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from callcenterapp.models import PhoneCall, CallDetail, JiraTriggerConfiguration


class DjangoRestFrameworkTests(APITestCase):

    def setUp(self):
        # data for which JIRA critera is met
        self.post_data_critera = {
            "action": "action_post",
            "name": "call_post",
            "data": {
                "id": 80,
                "event_timestamp": "2018-11-21T23:20:49Z",
                "queue_enter_time": "2018-11-21T23:20:52Z",
                "caller_id_num": "123_post",
                "caller_id_name": "johnnn_post",
                "queue_name": "queue_post",
                "queue_id": "4f6f3f76-4d5d-4f4b-a259-fd5d89e9c0ed",
                "session_id": "fa21bd8e-99fd-4452-83dd-ff261850646a",
                "event_name": "random",
                "recipient_id": "14fc164b-9322-4b3b-be64-ab08d7ba3bb8",
                "recipient_name": "Doe",
                "total_wait_time": 50
            }
        }

        # data for which JIRA critera is not met
        self.post_data_not_critera = {
            "action": "action_post",
            "name": "call_post",
            "data": {
                "id": 80,
                "event_timestamp": "2018-11-21T23:20:49Z",
                "queue_enter_time": "2018-11-21T23:20:52Z",
                "caller_id_num": "not_met",
                "caller_id_name": "not_met",
                "queue_name": "not_met",
                "queue_id": "4f6f3f76-4d5d-4f4b-a259-fd5d89e9c0ed",
                "session_id": "fa21bd8e-99fd-4452-83dd-ff261850646a",
                "event_name": "random",
                "recipient_id": "14fc164b-9322-4b3b-be64-ab08d7ba3bb8",
                "recipient_name": "Doe",
                "total_wait_time": 50
            }
        }

        self.config_data = {
            "total_wait_time": 100,
            "queue_name": "queue_post",
            "caller_id_name": "johnnn_post",
            "recipient_id": "14fc164b-9322-4b3b-be64-ab09d7ba3bb8"
        }

        call_detail_1 = CallDetail.objects.create(event_timestamp=timezone.now(),
                                                  queue_enter_time=timezone.now(),
                                                  caller_id_num='123',
                                                  caller_id_name='John', queue_name='queue_5',
                                                  queue_id='4f6f3f76-4d5d-4f4b-a259-fd5d89e9c0ed',
                                                  session_id='4f6f3f76-4d5d-4f4b-a259-fd5d89e9c0ed',
                                                  event_name='event_1',
                                                  recipient_id='4f6f3f76-4d5d-4f4b-a259-fd5d89e9c0ed',
                                                  recipient_name='xyz',
                                                  total_wait_time=500, )
        call_detail_2 = CallDetail.objects.create(event_timestamp=timezone.now(),
                                                  queue_enter_time=timezone.now(),
                                                  caller_id_num='987',
                                                  caller_id_name='Jane', queue_name='queue_5',
                                                  queue_id='4f6f3f76-4d5d-4f4b-a259-fd5d89e9c0ed',
                                                  session_id='4f6f3f76-4d5d-4f4b-a259-fd5d89e9c0ed',
                                                  event_name='event_2',
                                                  recipient_id='4f6f3f76-4d5d-4f4b-a259-fd5d89e9c0ed',
                                                  recipient_name='abc',
                                                  total_wait_time=500, )

        PhoneCall.objects.get_or_create(action="action_2600", name="call name 1", data=call_detail_1)
        PhoneCall.objects.get_or_create(action="action_2600", name="call name 2", data=call_detail_2)
        JiraTriggerConfiguration.objects.create(**self.config_data)

        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_list(self):
        response = self.client.get(reverse('call-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_create_jira_task_if_criteria_not_met(self):
        with mock.patch('callcenterapp.signals.jira_handler') as mocked_handler:
            response = self.client.post(reverse('call-list'), self.post_data_not_critera, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            post_save.connect(mocked_handler, sender=PhoneCall)

        self.assertEqual(mocked_handler.call_count, 0)

    def test_create_jira_task_if_criteria_met(self):
        with mock.patch('callcenterapp.signals.jira_handler') as mocked_handler:
            response = self.client.post(reverse('call-list'), self.post_data_critera, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            post_save.connect(mocked_handler, sender=PhoneCall)

        self.assertEqual(mocked_handler.call_count, 1)
