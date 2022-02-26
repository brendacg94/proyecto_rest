from rest_framework import serializers
from banks.models import *

class BankAccountSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length = 255, allow_blank = False)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    account_type = serializers.CharField(max_length = 255, allow_blank = False)
    user = serializers.IntegerField()
    bank = serializers.IntegerField()
