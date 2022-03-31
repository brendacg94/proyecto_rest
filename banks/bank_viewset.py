from banks.models import Bank, Account_type, Bank_account, Movement_type, Movement
from users.models import Usuario
from banks.serializers import BankAccountSerializer, BankSerializer, MovementSerializer
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

        accounts = Bank_account.objects.filter(id_user=saved_user).select_related("id_user","id_bank","id_account_type")
        if not accounts:
            return Response({'message': 'No tiene cuentas asignadas '}, status = status.HTTP_404_NOT_FOUND)
           
        result = { "accounts": list() }
        for acc in accounts:
            result["accounts"].append({
                "account_number": acc.account_number,
                "balance": acc.balance,
                "account_type": acc.id_account_type.name,
                "user_name": acc.id_user.names,
                "user_last_names": acc.id_user.last_names,
                "bank_name": acc.id_bank.name
            })

        return Response(result, status = status.HTTP_200_OK)

    @action(detail = False, methods = ['get','post'], url_path = 'bodyuseraccounts', url_name = 'bodyuseraccounts')
    def body_user_accounts(self, request):
        #id_user = request.query_params.get("id_user")
        id_user = str(request.data['id_user'])
        try:
            saved_user = Usuario.objects.get(pk=id_user)
        except Usuario.DoesNotExist as e:
            print(e)
            return Response({'message': 'No existe el usuario con id ' + id_user}, status = status.HTTP_404_NOT_FOUND)

        accounts = Bank_account.objects.filter(id_user=saved_user).select_related("id_user","id_bank","id_account_type")
        if not accounts:
            return Response({'message': 'No tiene cuentas asignadas '}, status = status.HTTP_404_NOT_FOUND)
           
        result = { "accounts": list() }
        for acc in accounts:
            result["accounts"].append({
                "account_number": acc.account_number,
                "balance": acc.balance,
                "account_type": acc.id_account_type.name,
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

        movement = Movement.objects.filter(bank_account=id_account).order_by('-creation_movement').first()
        
        if movement:
            format = "%d/%m/%Y %H:%M:%S"
            time = movement.creation_movement.strftime(format)

        else:
            time = "---"

        result = { 
                "account_number": account.account_number,
                "balance": account.balance,
                "last_movement":time,
                "account_type": account.id_account_type.name,
                "user_name": account.id_user.names,
                "user_last_names": account.id_user.last_names,
                "bank_name": account.id_bank.name
        }
    
        return Response(result, status = status.HTTP_200_OK)
        
    @action(detail = False, methods = ['get'], url_path = 'listaccounts', url_name = 'listaccounts')
    def list_accounts(self, request):
        accounts = Bank_account.objects.all().select_related("id_user","id_bank","id_account_type")
        result = { "accounts": list() }
        for acc in accounts:
            result["accounts"].append({
                "id": acc.id,
                "account_number": acc.account_number,
                "balance": acc.balance,
                "account_type": acc.id_account_type.name,
                "user_name": acc.id_user.names,
                "user_last_names": acc.id_user.last_names,
                "bank_name": acc.id_bank.name
            })

        return Response(result, status = status.HTTP_200_OK)

    @action(detail = False, methods = ['post'], url_path = 'createaccount', url_name = 'createaccount')
    def create_account(self, request):
        account_serializer = BankAccountSerializer(data = request.data)
        
        if not account_serializer.is_valid():
            return Response({'message':'Hay errores en la información enviada'},
                            status = status.HTTP_400_BAD_REQUEST)

        account_number = request.data['account_number']
        account = Bank_account.objects.filter(account_number=account_number)

        #account_type = account_serializer.validated_data.get("account_type")
        #print(account_type)

        if account.exists():
            return Response({'message':'Este numero de cuenta ya se ha registrado'},
                            status = status.HTTP_400_BAD_REQUEST)

        id_user = str(account_serializer.validated_data.get("id_user"))
        print(id_user)

        try:
            saved_user = Usuario.objects.get(pk=id_user)
        except Usuario.DoesNotExist as e:
            print(e)
            return Response({'message': 'No existe el usuario con id ' + id_user}, 
                            status = status.HTTP_404_NOT_FOUND)

        id_bank = str(account_serializer.validated_data.get("id_bank"))

        try:
            saved_bank = Bank.objects.get(pk=id_bank)
        except Bank.DoesNotExist as e:
            print(e)
            return Response({'message': 'No existe el banco con id ' + id_bank}, 
                            status = status.HTTP_404_NOT_FOUND)

        id_account_type = str(account_serializer.validated_data.get("id_account_type"))

        try:
            saved_account_type = Account_type.objects.get(pk=id_account_type)
        except Account_type.DoesNotExist as e:
            print(e)
            return Response({'message': 'No existe el tipo de cuenta con id ' + id_account_type}, 
                            status = status.HTTP_404_NOT_FOUND)

        account = Bank_account(
            account_number = account_serializer.validated_data.get("account_number"),
            #account_type = account_serializer.validated_data.get("account_type"),
            id_user = saved_user,
            id_bank = saved_bank,
            id_account_type = saved_account_type
        )
        account.save()

        return Response(account_serializer.data,status = status.HTTP_200_OK)

    @action(detail = False, methods = ['delete'], url_path = 'deleteaccount', url_name = 'deleteaccount')
    def delete_account(self, request):
        id_account = request.query_params.get("id_account")
        account = Bank_account.objects.filter(id=id_account).first()
        
        if account:
            account.delete()
            return Response({'message':'Cuenta eliminada correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'No existe una cuenta con id ' + id_account},status = status.HTTP_400_BAD_REQUEST)

    #BANK 

    @action(detail = False, methods = ['get'], url_path = 'bankdetail', url_name = 'bankdetail')
    def bank_detail(self, request):
        id_bank = request.query_params.get("id_bank")
        bank = Bank.objects.filter(id=id_bank).first()

        if not bank:
            return Response({'message': 'No existe el banco con id ' + id_bank}, status = status.HTTP_404_NOT_FOUND)
       
        result = { 
                "id": bank.id,
                "name": bank.name
        }
    
        return Response(result, status = status.HTTP_200_OK)

    @action(detail = False, methods = ['get'], url_path = 'listbanks', url_name = 'listbanks')
    def list_banks(self, request):
        banks = Bank.objects.all()

        result = { "banks": list() }
        for ban in banks:
            result["banks"].append({
                "id": ban.id,
                "name": ban.name
            })

        return Response(result, status = status.HTTP_200_OK)

    @action(detail = False, methods = ['post'], url_path = 'createbank', url_name = 'createbank')
    def create_bank(self, request):
        serializer = BankSerializer(data = request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response(serializer.errors,
                status = status.HTTP_400_BAD_REQUEST)

        name = request.data['name']
        bank = Bank.objects.filter(name=name)

        if bank.exists():
            return Response({'message':'Este banco ya ha sido registrado'},
                            status = status.HTTP_400_BAD_REQUEST)

        bank = Bank(
            name = serializer.validated_data.get("name")
        )
        bank.save()

        return Response(serializer.data,status = status.HTTP_200_OK)

    @action(detail = False, methods = ['put'], url_path = 'updatebank', url_name = 'updatebank')
    def update_bank(self, request):
        serializer = BankSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                status = status.HTTP_400_BAD_REQUEST)

        id_bank = request.query_params.get("id_bank")
        bank = Bank.objects.filter(id=id_bank).first()

        if not bank:
            return Response({'message': 'No existe el banco con id ' + id_bank}, 
                            status = status.HTTP_404_NOT_FOUND)

        name = request.data['name']
        bank_name = Bank.objects.filter(name=name)

        if bank_name.exists():
            return Response({'message':'Este banco ya ha sido registrado'},
                            status = status.HTTP_400_BAD_REQUEST)

        bank.name = request.data['name']
        bank.save()

        return Response(serializer.data,status = status.HTTP_200_OK)    

    @action(detail = False, methods = ['delete'], url_path = 'deletebank', url_name = 'deletebank')
    def delete_bank(self, request):
        id_bank = request.query_params.get("id_bank")
        bank = Bank.objects.filter(id=id_bank).first()
        
        if bank:
            bank.delete()
            return Response({'message':'Banco eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'No existe un banco con id ' + id_bank},status = status.HTTP_400_BAD_REQUEST)

    #MOVEMENT

    @action(detail = False, methods = ['post'], url_path = 'createmovement', url_name = 'createmovement')
    def create_movement(self, request):
        serializer = MovementSerializer(data = request.data)
        
        if not serializer.is_valid():
            return Response({'message':'Hay errores en la información enviada'},
                            status = status.HTTP_400_BAD_REQUEST)

        movement_type = str(serializer.validated_data.get("movement_type"))

        try:
            saved_movement_type = Movement_type.objects.get(pk=movement_type)
        except Movement_type.DoesNotExist as e:
            print(e)
            return Response({'message': 'No existe el tipo de movimmiento con id ' + movement_type}, 
                            status = status.HTTP_404_NOT_FOUND)

        bank_account = str(serializer.validated_data.get("bank_account"))

        try:
            saved_bank_account = Bank_account.objects.get(pk=bank_account)
        except Bank_account.DoesNotExist as e:
            print(e)
            return Response({'message': 'No existe la cuenta de banco con id ' + bank_account}, 
                            status = status.HTTP_404_NOT_FOUND)

        balance = saved_bank_account.balance
        print(balance)
        quantity = serializer.validated_data.get("quantity")
        movement_type = serializer.validated_data.get("movement_type")


        if movement_type == 1:
            balance = balance + quantity
            print(balance)

            saved_bank_account.balance = balance
            saved_bank_account.save()
    
            new_movement = Movement(
                quantity = serializer.validated_data.get("quantity"),
                movement_type = saved_movement_type,
                available_balance = balance,
                bank_account = saved_bank_account
            )
            new_movement.save()

        elif movement_type == 2:
            if balance < quantity:
                 return Response({'message':'Tu cuenta tiene insuficientes fondos para realizar esta operación'},
                            status = status.HTTP_400_BAD_REQUEST)

            balance = balance - quantity
            print(balance)

            saved_bank_account.balance = balance
            saved_bank_account.save()
    
            new_movement = Movement(
                quantity = serializer.validated_data.get("quantity"),
                movement_type = saved_movement_type,
                available_balance = balance,
                bank_account = saved_bank_account
            )
            new_movement.save()

        result = { 
                "bank_account": saved_bank_account.account_number,
                "movement_type": saved_movement_type.name,
                "quantity": request.data['quantity'],
                "balance": balance
        }

        return Response(result,status = status.HTTP_200_OK)

    @action(detail = False, methods = ['get'], url_path = 'movementhistory', url_name = 'movementhistory')
    def movement_history(self, request):
        id_account = request.query_params.get("id_account")
        try:
            saved_account = Bank_account.objects.get(pk=id_account)
        except Bank_account.DoesNotExist as e:
            print(e)
            return Response({'message': 'No existe la cuenta de banco con id ' + id_account}, 
                            status = status.HTTP_404_NOT_FOUND)

        movements = Movement.objects.filter(bank_account=saved_account).order_by('-creation_movement').select_related("movement_type","bank_account")
        if not movements:
            return Response({'message': 'Esta cuenta de banco no tiene movimientos registrados'}, 
                            status = status.HTTP_404_NOT_FOUND)

        result = { "movements": list() }
        for mov in movements:
            format = "%d/%m/%Y %H:%M:%S"
            time = mov.creation_movement.strftime(format)
            result["movements"].append({
                "bank_account": mov.bank_account.account_number,
                "creation_movement": time,
                "movement_type": mov.movement_type.name,
                "quantity": mov.quantity,
                "available_balance": mov.available_balance
            })

        return Response(result, status = status.HTTP_200_OK)



    



     

            
        
