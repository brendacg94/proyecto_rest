from Bank_account.models import Bank_account
from Bank_account.serializers import Bank_accountSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

class Bank_accountViewSet(viewsets.ViewSet):

    def list(self,request):
        queryset = Bank_account.objects.all()
        serializer = Bank_accountSerializer(queryset, many = True)
        return Response(serializer.data,status = status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        bank_account = Bank_account.objects.filter(id = pk).first()
        bank_account_serializer = Bank_accountSerializer(bank_account)
        return Response(bank_account_serializer.data,status = status.HTTP_200_OK)

    def create(self,request):
        bank_account_serializer = Bank_accountSerializer(data = request.data)
        if bank_account_serializer.is_valid():
            bank_account_serializer.save()
            return Response(bank_account_serializer.data,status = status.HTTP_201_CREATED)
        return Response(bank_account_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        bank_account = Bank_account.objects.filter(id = pk).first()
        bank_account_serializer = Bank_accountSerializer(bank_account,data = request.data)
        if bank_account_serializer.is_valid():
                bank_account_serializer.save()
                return Response(bank_account_serializer.data,status = status.HTTP_200_OK)
        return Response(bank_account_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        bank_account = Bank_account.objects.filter(id = pk).first()
        if bank_account:
            bank_account.delete()
            return Response({'message':'Cuenta de banco eliminada correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'No existe una Cuenta de banco con estos datos'},status = status.HTTP_400_BAD_REQUEST)
