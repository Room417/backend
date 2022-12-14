from rest_framework.routers import SimpleRouter

from .views import *


router = SimpleRouter()
router.register('persons/residents', ResidentsViewSet, basename='residents')
router.register('persons/students', StudentViewSet, basename='students')
router.register('persons/staff', StaffViewSet, basename='staff')


urlpatterns = router.urls
