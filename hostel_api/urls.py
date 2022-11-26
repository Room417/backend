from django.urls import path

from .views import *


urlpatterns = [
    path('persons/staff:custom-search', StaffViewSet.as_view({'post': 'search'}),
         name='persons-staff-custom-search'),
    path('persons/staff:search', StaffViewSet.as_view({'post': 'all_search'}),
         name='persons-staff-search'),

    path('persons/students:search', StudentViewSet.as_view({'post': 'search'}),
         name='persons-students-search'),
    path('persons/students:search-one', StudentViewSet.as_view({'post': 'search_one'}),
         name='persons-students-search-one'),

    path('persons/residents:custom-search', ResidentsViewSet.as_view({'post': 'search'}),
         name='persons-residents-custom-search'),
    path('persons/residents:search', ResidentsViewSet.as_view({'post': 'all_search'}),
         name='persons-residents-search'),
    path('persons/residents:search-one', ResidentsViewSet.as_view({'post': 'search_one'}),
         name='persons-residents-search-one'),
    path('persons/residents', ResidentsViewSet.as_view({'post': 'create'}),
         name='persons-residents-create'),
    path('residents/relocate', ResidentsViewSet.as_view({'post': 'relocate'}),
         name='persons-residents-relocate'),
]
