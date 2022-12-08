from rest_framework import serializers

from .models import Notification, Request
from hostel_api.serializers import StaffSerializer, ResidentSerializer


class NotificationSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    recipients = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'author',
            'title',
            'description',
            'creation_date',
            'is_published',
            'recipients',
            'start_date',
            'end_date',
            'is_active'
        ]

    def get_author(self, obj):
        include_fields = self.context.get('include')
        if include_fields and 'author' in include_fields:
            return StaffSerializer(obj.author).data

        return obj.author.__str__()

    def get_recipients(self, obj):
        include_fields = self.context.get('include')
        if include_fields and 'recipients' in include_fields:
            return ResidentSerializer(obj.recipients.all(), many=True).data

        return [item.__str__() for item in obj.recipients.all()]


class NotificationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            'author',
            'title',
            'description',
            'creation_date',
            'is_published',
            'recipients',
            'start_date',
            'end_date',
            'is_active'
        ]


class RequestSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    recipients = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = [
            'id',
            'author',
            'recipients',
            'title',
            'description',
            'creation_date',
            'is_seen',
            'archived',
            'is_provided',
            'provision_date',
        ]

    def get_author(self, obj):
        include_fields = self.context.get('include')
        if include_fields and 'author' in include_fields:
            return ResidentSerializer(obj.author).data

        return obj.author.__str__()

    def get_recipients(self, obj):
        include_fields = self.context.get('include')
        if include_fields and 'recipients' in include_fields:
            return StaffSerializer(obj.recipients.all(), many=True).data

        return [item.__str__() for item in obj.recipients.all()]


class RequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = [
            'author',
            'recipients',
            'title',
            'description',
        ]
