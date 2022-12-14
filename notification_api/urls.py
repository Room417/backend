from rest_framework.routers import SimpleRouter

from .views import *


router = SimpleRouter()
router.register('notifications', NotificationViewSet, basename='notifications')
router.register('requests', NotificationViewSet, basename='requests')


urlpatterns = router.urls
