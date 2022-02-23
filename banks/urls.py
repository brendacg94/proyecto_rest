from rest_framework.routers import DefaultRouter
from banks.bank_viewset import BankViewSet

router = DefaultRouter()
router.register(r'', BankViewSet, basename='bank')
urlpatterns = router.urls