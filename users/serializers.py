from rest_framework import serializers
from users.models import Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    email = serializers.EmailField(required = True)
    names = serializers.CharField(max_length = 255, required = True)
    last_names = serializers.CharField(max_length = 255, required = True)
    password = serializers.CharField(max_length = 255, required = True)
    password1 = serializers.CharField(max_length = 255, required = True)

class UserUpdateSerializer(serializers.Serializer):

    email = serializers.EmailField(required = False)
    names = serializers.CharField(max_length = 255, required = False)
    last_names = serializers.CharField(max_length = 255, required = False)
    password = serializers.CharField(max_length = 255, required = False)
    password1 = serializers.CharField(max_length = 255, required = False)

    


