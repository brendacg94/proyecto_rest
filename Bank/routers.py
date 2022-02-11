from rest_framework.routers import DefaultRouter
from Bank.bank_viewsets import BankViewSet

router = DefaultRouter()
router.register(r'banks', BankViewSet, basename='bank')
urlpatterns = router.urls