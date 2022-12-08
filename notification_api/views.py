from rest_framework.permissions import IsAuthenticated

from hostel_api.mixins import DefaultViewMixin
from .models import Notification, Request
from .serializers import NotificationSerializer, RequestSerializer


class NotificationViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными работников общежития """
    model = Notification
    serializer_class = NotificationSerializer
    list_serializer = NotificationSerializer
    detail_serializer = NotificationSerializer
    default_sort_fields = ['-start_date']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        author_id = self.request.user.staff.id

        return self.model.objects.filter(author_id=author_id)


class RequestsViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными работников общежития """
    model = Request
    serializer_class = RequestSerializer
    list_serializer = RequestSerializer
    detail_serializer = RequestSerializer
    default_sort_fields = ['-start_date']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        recipient = self.request.user.staff

        return self.model.objects.filter(recipients__in=[recipient])
