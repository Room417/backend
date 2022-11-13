from hostel_api.mixins import DefaultViewMixin
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(DefaultViewMixin):
    """ ViewSet для взаимодействия с данными работников общежития """
    model = Notification
    serializer_class = NotificationSerializer
    default_sort_fields = ['-start_date']
