from rest_framework import serializers
from Bank_account.models import Bank_account

class Bank_accountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank_account
        fields = '__all__'

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'account number': instance.account_number,
            'balance': instance.balance,
            'names': instance.id_user.names,
            'last names': instance.id_user.last_names,
            'bank':instance.id_bank.name
        }