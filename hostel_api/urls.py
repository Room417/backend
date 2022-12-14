from rest_framework.routers import SimpleRouter

from .views import *


router = SimpleRouter()
router.register('persons', ResidentsViewSet, basename='residents')
router.register('persons', StudentViewSet, basename='students')
router.register('persons', StaffViewSet, basename='staff')


urlpatterns = router.urls
