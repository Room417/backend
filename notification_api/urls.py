from django.urls import path

from .views import *


urlpatterns = [
    path('notifications:search', NotificationViewSet.as_view({'post': 'search'}),
         name='notification-search'),
    path('notifications:search-one', NotificationViewSet.as_view({'post': 'search_one'}),
         name='notification-search-one'),


    path('requests:search', RequestsViewSet.as_view({'post': 'search'}),
         name='requests-search'),
    path('requests:search-one', RequestsViewSet.as_view({'post': 'search_one'}),
         name='requests-search-one'),
]
