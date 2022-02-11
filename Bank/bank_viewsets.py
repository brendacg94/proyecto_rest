from Bank.models import Bank
from Bank.serializers import BankSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

class BankViewSet(viewsets.ViewSet):

    def list(self,request):
        queryset = Bank.objects.all()
        serializer = BankSerializer(queryset, many = True)
        return Response(serializer.data,status = status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        bank = Bank.objects.filter(id = pk).first()
        bank_serializer = BankSerializer(bank)
        return Response(bank_serializer.data,status = status.HTTP_200_OK)

    def create(self,request):
        bank_serializer = BankSerializer(data = request.data)
        if bank_serializer.is_valid():
            bank_serializer.save()
            return Response(bank_serializer.data,status = status.HTTP_201_CREATED)
        return Response(bank_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        bank = Bank.objects.filter(id = pk).first()
        bank_serializer = BankSerializer(bank,data = request.data)
        if bank_serializer.is_valid():
                bank_serializer.save()
                return Response(bank_serializer.data,status = status.HTTP_200_OK)
        return Response(bank_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        bank = Bank.objects.filter(id = pk).first()
        if bank:
            bank.delete()
            return Response({'message':'Banco eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'No existe un Banco con estos datos'},status = status.HTTP_400_BAD_REQUEST)

                
        
