from rest_framework import serializers
from users.models import Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    #email = serializers.EmailField(required = True)
    #names = serializers.CharField(max_length = 255, required = True)
    #last_names = serializers.CharField(max_length = 255, required = True)

    def create(self,validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self,instance,validated_data):
        updated_user = super().update(instance,validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


