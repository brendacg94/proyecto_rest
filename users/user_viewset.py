from users.models import Usuario
from users.serializers import UserSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

class UserViewSet(viewsets.ViewSet):

    @action(detail = False, methods = ['get'], url_path = 'userdetail', url_name = 'userdetail')
    def user_detail(self, request):
        id_user = request.query_params.get("id_user")
        user = Usuario.objects.filter(id=id_user).first()

        if not user:
            return Response({'message': 'No existe el usuario con id ' + id_user}, status = status.HTTP_404_NOT_FOUND)
       
        result = { 
                "id": user.id,
                "email": user.email,
                "names": user.names,
                "last_names": user.last_names
        }
    
        return Response(result, status = status.HTTP_200_OK)

    @action(detail = False, methods = ['get'], url_path = 'userslist', url_name = 'userslist')
    def users_list(self, request):
        users = Usuario.objects.all()
        result = { "users": list() }
        for user in users:
            result["users"].append({
                "id": user.id,
                "email": user.email,
                "names": user.names,
                "last_names": user.last_names
            })

        return Response(result, status = status.HTTP_200_OK)

    def create(self,request):
        user_serializer = UserSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data,status = status.HTTP_201_CREATED)
        return Response(user_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    @action(detail = False, methods = ['post'], url_path = 'createuser', url_name = 'createuser')
    def create_user(self, request):
        serializer = UserSerializer(data = request.data)
        
        if not serializer.is_valid():
            return Response({'message':'Hay errores en la información enviada'},
                            status = status.HTTP_400_BAD_REQUEST)

        #account_number = request.data['account_number']
        #account = Bank_account.objects.filter(account_number=account_number)

        #account_type = account_serializer.validated_data.get("account_type")
        #print(account_type)

        #if account.exists():
            #return Response({'message':'Este numero de cuenta ya se ha registrado'},
                            #status = status.HTTP_400_BAD_REQUEST)

        return Response({'message':'Prueba'},status = status.HTTP_200_OK)

    def update(self,request,pk=None):
        user = Usuario.objects.filter(id = pk).first()
        user_serializer = UserSerializer(user,data = request.data)
        if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data,status = status.HTTP_200_OK)
        return Response(user_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    @action(detail = False, methods = ['delete'], url_path = 'deleteuser', url_name = 'deleteuser')
    def delete_user(self, request):
        id_user = request.query_params.get("id_user")
        user = Usuario.objects.filter(id=id_user).first()
        
        if user:
            user.delete()
            return Response({'message':'Usuario eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'No existe un usuario con id ' + id_user},status = status.HTTP_400_BAD_REQUEST)


                
        
