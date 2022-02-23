from rest_framework.routers import DefaultRouter
from users.user_viewset import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
urlpatterns = router.urls

