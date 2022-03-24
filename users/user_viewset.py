from users.models import Usuario
from users.serializers import UserSerializer, UserUpdateSerializer
from django.contrib.auth.hashers import make_password
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

    @action(detail = False, methods = ['post'], url_path = 'createuser', url_name = 'createuser')
    def create_user(self, request):
        serializer = UserSerializer(data = request.data)
        
        if not serializer.is_valid():
            return Response({'message':'Hay errores en la información enviada'},
                            status = status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get("email")
        user = Usuario.objects.filter(email=email)

        if user.exists():
            return Response({'message':'Este correo electrónico ya se ha registrado'},
                            status = status.HTTP_400_BAD_REQUEST)

        password = request.data['password']
        password1 = request.data['password1']

        if password != password1:
            return Response({'password':'Debe ingesar ambas contraseñas iguales'},
                            status = status.HTTP_400_BAD_REQUEST)


        new_user = Usuario(
            email = email,
            names = serializer.validated_data.get("names"),
            last_names = serializer.validated_data.get("last_names")
        )
        new_user.set_password(request.data['password'])
        new_user.save()

        result = { 
                "email": request.data['email'],
                "names": request.data['names'],
                "last_names": request.data['last_names']
                #"password": make_password(request.data['password'])
        }

        return Response(result,status = status.HTTP_200_OK)

    @action(detail = False, methods = ['put'], url_path = 'updateuser', url_name = 'updateuser')
    def update_user(self, request):
        serializer = UserUpdateSerializer(data = request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status = status.HTTP_400_BAD_REQUEST)

        id_user = request.query_params.get("id_user")
        user = Usuario.objects.filter(id=id_user).first()

        if not user:
            return Response({'message': 'No existe el usuario con id ' + id_user}, 
                            status = status.HTTP_404_NOT_FOUND)                 

        email = serializer.validated_data.get("email")
        email_user = Usuario.objects.filter(email=email)

        if email_user.exists():
            return Response({'message':'Este correo electrónico ya se ha registrado'},
                            status = status.HTTP_400_BAD_REQUEST)

        user.email = email
        user.names = request.data['names']
        user.last_names = request.data['last_names']
        user.set_password(request.data['password'])
        user.save()

        return Response(serializer.data,status = status.HTTP_200_OK)

    @action(detail = False, methods = ['delete'], url_path = 'deleteuser', url_name = 'deleteuser')
    def delete_user(self, request):
        id_user = request.query_params.get("id_user")
        user = Usuario.objects.filter(id=id_user).first()
        
        if user:
            user.delete()
            return Response({'message':'Usuario eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'No existe un usuario con id ' + id_user},status = status.HTTP_400_BAD_REQUEST)


                
        
