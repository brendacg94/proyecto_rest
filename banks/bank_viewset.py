from banks.models import *
from users.models import Usuario
#from users.serializers import UserSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

class BankViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='useraccounts', url_name='useraccounts')
    def user_accounts(self, request):
        id_user = request.query_params.get("id_user")
        try:
            saved_user = Usuario.objects.get(pk=id_user)
        except Usuario.DoesNotExist as e:
            print(e)
            return Response({'message': 'No existe el usuario con id ' + id_user}, status = status.HTTP_404_NOT_FOUND)

        accounts = Bank_account.objects.filter(id_user=saved_user).select_related("id_user","id_bank")
        result = { "accounts": list() }
        for acc in accounts:
            result["accounts"].append({
                "account_number": acc.account_number,
                "balance": acc.balance,
                "account_type": acc.account_type,
                "user_name": acc.id_user.names,
                "user_last_names": acc.id_user.last_names,
                "bank_name": acc.id_bank.name
            })

        return Response(result, status = status.HTTP_200_OK)
     
     
            
        
