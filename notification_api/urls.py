from django.urls import path

from .views import *


urlpatterns = [
    path('notifications:search', NotificationViewSet.as_view({'post': 'search'}),
         name='notification-search'),
    path('notifications:search-one', NotificationViewSet.as_view({'post': 'search_one'}),
         name='notification-search-one'),
    path('notifications', NotificationViewSet.as_view({'post': 'create'}),
         name='notification-create'),
    path('notifications/{pk}/$', NotificationViewSet.as_view({'patch': 'partial_update'}),
         name='notifications-update'),
    path('notifications/{pk}/$', NotificationViewSet.as_view({'delete': 'destroy'}),
         name='notifications-delete'),


    path('requests:search', RequestsViewSet.as_view({'post': 'search'}),
         name='requests-search'),
    path('requests:search-one', RequestsViewSet.as_view({'post': 'search_one'}),
         name='requests-search-one'),
    path('requests', RequestsViewSet.as_view({'post': 'create'}),
         name='requests-create'),
    path('requests/{pk}/$', RequestsViewSet.as_view({'patch': 'partial_update'}),
         name='requests-update'),
    path('requests/{pk}/$', RequestsViewSet.as_view({'delete': 'destroy'}),
         name='requests-delete'),
]
