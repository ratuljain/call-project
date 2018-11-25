# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from callcenterapp.models import PhoneCall, JiraTriggerConfiguration
from callcenterapp.serializers import PhoneCallSerializer, JiraTriggerConfigurationSerializer


class CallCenterService(APIView):
    """
        List all calls, or create a new call.
    """

    def get(self, request, format=None):
        calls = PhoneCall.objects.all()
        serializer = PhoneCallSerializer(calls, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a new PhoneCall entry to the DB.
        A post save signal is also sent to check if the call meets certain criteria.
        """
        serializer = PhoneCallSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JiraConfiguration(APIView):
    """
        List all calls, or create a new call.
    """

    def get(self, request, format=None):
        calls = JiraTriggerConfiguration.objects.all()
        serializer = JiraTriggerConfigurationSerializer(calls, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a new PhoneCall entry to the DB.
        A post save signal is also sent to check if the call meets certain criteria.
        """
        serializer = JiraTriggerConfigurationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
