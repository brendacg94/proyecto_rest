from rest_framework.routers import DefaultRouter
from Bank_account.bank_account_viewsets import Bank_accountViewSet

router = DefaultRouter()
router.register(r'bank_accounts', Bank_accountViewSet, basename='bank_account')
urlpatterns = router.urls