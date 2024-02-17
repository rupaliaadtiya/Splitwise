from rest_framework import serializers
from account import models
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import logging

class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'mobile', 'password')
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        user = models.User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            mobile=validated_data['mobile'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = models.User
        fields = ('email', 'password')

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password. Please try again.")

        refresh = RefreshToken.for_user(user)

        data['user'] = user
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)

        return data
