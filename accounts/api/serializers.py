from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from ..models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.encoding import force_str, force_bytes, smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'password', 'password2']

    def save(self):
        username = self.validated_data.get('username')
        email = self.validated_data.get("email")
        avatar = self.validated_data.get('data')
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')

        if password != password2:
            raise serializers.ValidationError({"error": "password's does not match."})

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': "A user with that username already exists."})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "A user with that email already exists."})

        user = User.objects.create(username=username, email=email, avatar=avatar)
        user.set_password(password)
        user.save()

        return user

class PasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    old_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']

class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']
    