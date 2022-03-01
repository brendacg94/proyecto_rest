from rest_framework import serializers
from banks.models import *
from users.models import Usuario

class BankAccountSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length = 255, allow_blank = False)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    account_type = serializers.CharField(max_length = 255, allow_blank = False)
    id_user = serializers.IntegerField()
    id_bank = serializers.IntegerField()

    def validate(self, data):
        account_number = data['account_number']
        account = Bank_account.objects.filter(account_number=account_number)
        if account.exists():
            raise ValidationError("Este numero de cuenta ya se ha registrado")

    def validate_account_number(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar un número de cuenta")
        return value

    def validate_balance(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar una cantidad de dinero")
        return value

    def validate_account_type(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar el tipo de cuenta")
        return value

    def validate_id_user(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar el id del usuario")
        return value

    def validate_id_bank(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar el id del banco")
        return value


    #def validate_id_user(self, value):
     #   data = self.get_initial()
      #  id_user = data.get("id_user")
       # user = Usuario.objects.filter(id=id_user)
        #if user.DoesNotExist():
         #   raise ValidationError("El id de usuario no existe")
        #return value


class BankSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 255, allow_blank = False)
