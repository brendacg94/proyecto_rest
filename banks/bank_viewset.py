from banks.models import *
from users.models import Usuario
from banks.serializers import BankAccountSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

class BankViewSet(viewsets.ViewSet):

    #BANK ACCOUNT

    @action(detail = False, methods = ['get'], url_path = 'useraccounts', url_name = 'useraccounts')
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

    @action(detail = False, methods = ['get'], url_path = 'accountdetail', url_name = 'accountdetail')
    def account_detail(self, request):
        id_account = request.query_params.get("id_account")
        account = Bank_account.objects.filter(id=id_account).first()

        if not account:
            return Response({'message': 'No existe la cuenta con id ' + id_account}, status = status.HTTP_404_NOT_FOUND)
       
        result = { 
                "account_number": account.account_number,
                "balance": account.balance,
                "account_type": account.account_type,
                "user_name": account.id_user.names,
                "user_last_names": account.id_user.last_names,
                "bank_name": account.id_bank.name
        }
    
        return Response(result, status = status.HTTP_200_OK)
        
    @action(detail = False, methods = ['get'], url_path = 'listaccounts', url_name = 'listaccounts')
    def list_accounts(self, request):
        accounts = Bank_account.objects.all().select_related("id_user","id_bank")
        result = { "accounts": list() }
        for acc in accounts:
            result["accounts"].append({
                "id": acc.id,
                "account_number": acc.account_number,
                "balance": acc.balance,
                "account_type": acc.account_type,
                "user_name": acc.id_user.names,
                "user_last_names": acc.id_user.last_names,
                "bank_name": acc.id_bank.name
            })

        return Response(result, status = status.HTTP_200_OK)

    @action(detail = False, methods = ['post'], url_path = 'createaccount', url_name = 'createaccount')
    def create_account(self, request):
        account_serializer = BankAccountSerializer(data = request.data)
        
        if account_serializer.is_valid():
            account_serializer.save()
            return Response({'message':'Cuenta registrada correctamente'},status = status.HTTP_201_CREATED)
        return Response({'message':'Hay errores en la información enviada'},status = status.HTTP_400_BAD_REQUEST)

    @action(detail = False, methods = ['delete'], url_path = 'deleteaccount', url_name = 'deleteaccount')
    def delete_account(self, request):
        id_account = request.query_params.get("id_account")
        account = Bank_account.objects.filter(id=id_account).first()
        
        if account:
            account.delete()
            return Response({'message':'Cuenta eliminada correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'No existe una cuenta con id ' + id_account},status = status.HTTP_400_BAD_REQUEST)

    #BANK 

    

     

            
        
