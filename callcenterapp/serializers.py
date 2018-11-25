from rest_framework import serializers

from callcenterapp.models import CallDetail, PhoneCall, JiraTriggerConfiguration


class CallDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallDetail
        fields = ('id', 'event_timestamp', 'queue_enter_time', 'caller_id_num', 'caller_id_name', 'queue_name',
                  'queue_id', 'session_id', 'event_name', 'recipient_id', 'recipient_name', 'total_wait_time',)


class PhoneCallSerializer(serializers.ModelSerializer):
    data = CallDetailSerializer(required=True)

    def create(self, validated_data):
        call_details_data = validated_data.pop('data')
        call_detail = CallDetail.objects.create(**call_details_data)
        phone_call = PhoneCall.objects.create(data=call_detail, **validated_data)

        return phone_call

    class Meta:
        model = PhoneCall
        fields = ('id', 'action', 'name', 'data',)


class JiraTriggerConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JiraTriggerConfiguration
        fields = ('total_wait_time', 'queue_name', 'caller_id_name', 'recipient_id',)


# Serializers for the JIRA request object.
class ProjectSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class IssueSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class FieldsSerializer(serializers.Serializer):
    project = ProjectSerializer()
    summary = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    issuetype = IssueSerializer()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class JiraIssueSerializer(serializers.Serializer):
    fields = FieldsSerializer()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
