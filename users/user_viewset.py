from users.models import Usuario
from users.serializers import UserSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):

    def list(self,request):
        queryset = Usuario.objects.all()
        serializer = UserSerializer(queryset, many = True)
        return Response(serializer.data,status = status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = Usuario.objects.filter(id = pk).first()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data,status = status.HTTP_200_OK)

    def create(self,request):
        user_serializer = UserSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data,status = status.HTTP_201_CREATED)
        return Response(user_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        user = Usuario.objects.filter(id = pk).first()
        user_serializer = UserSerializer(user,data = request.data)
        if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data,status = status.HTTP_200_OK)
        return Response(user_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        user = Usuario.objects.filter(id = pk).first()
        if user:
            user.delete()
            return Response({'message':'Usuario eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'No existe un Usuario con estos datos'},status = status.HTTP_400_BAD_REQUEST)

                
        
