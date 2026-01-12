from rest_framework import serializers
from .models import *


class loginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'}, write_only = True)


class UserSerializer(serializers.ModelSerializer): 
    name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    user_role = serializers.CharField(max_length=30)
    password = serializers.CharField(min_length=5)
    class Meta:
        model = Users
        fields = '__all__'

    # def validate(self, attrs):
    #     return attrs