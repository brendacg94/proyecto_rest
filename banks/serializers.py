from rest_framework import serializers
from banks.models import *
from users.models import Usuario

class BankAccountSerializer(serializers.Serializer):
    account_number = serializers.IntegerField( required = True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default = 0, required = False)
    #account_type = serializers.CharField(max_length = 255, required = True)
    id_user = serializers.IntegerField(required = True)
    id_bank = serializers.IntegerField()
    id_account_type = serializers.IntegerField(required = True)

class BankSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 255, required = True)

class MovementSerializer(serializers.Serializer):
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, required = True)
    #movement_type = serializers.CharField(max_length = 255, required = True)
    movement_type = serializers.IntegerField(required = True)
    bank_account = serializers.IntegerField(required = True)
