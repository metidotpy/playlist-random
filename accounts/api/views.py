from django.shortcuts import reverse
from rest_framework import serializers, views
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    TokenObtainPairSerializer,
    RegisterSerializer,
    PasswordChangeSerializer,
    ProfileSerializer,
)
from .permissions import IsAnonymous
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import DjangoUnicodeDecodeError, force_str, force_bytes, smart_bytes, smart_str
from ..models import User
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os
from django.http import HttpResponsePermanentRedirect
from rest_framework import generics

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RegisterView(views.APIView):
    permission_classes = [IsAnonymous]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            user = serializer.save()
            current_site = get_current_site(request)
            data['response'] = "Registration is success."
            data['username'] = user.username
            data['email'] = user.email
            token = RefreshToken.for_user(user=user)
            data['token'] = {
                'refresh': str(token),
                'access': str(token.access_token),
            }
            mail_subject = "Email confirmation"
            message = render_to_string(
                'email-temp.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            to_email = data['email']
            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email]
            )
            email.send()
            data['confirmation_email'] = "Confirmation mail sended to your mail."
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return Response({"verify": "your account verified."})
    else:
        return Response({"error": "your account not verified."})


class PasswordChangeView(views.APIView):
    permission_classess = [IsAuthenticated]

    def put(self, request):
        self.user = User.objects.get(pk = self.request.user.pk)
        serializer = PasswordChangeSerializer(self.user, data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            password = serializer.validated_data.get('password')
            password2 = serializer.validated_data.get('password2')
            if not self.user.check_password(old_password):
                raise serializers.ValidationError({'old_password': 'wrong password.'})

            if password != password2:
                raise serializers.ValidationError({'error': 'password does not match.'})
            
            self.user.set_password(password)
            self.user.save()
            return Response({"password_change": "password changed successful."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Profile(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get(self, request):
        try:
            self.user = request.user
            user = User.objects.get(pk = self.user.pk)
        except User.DoesNotExist:
            return Response({'error': "not found."}, status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def put(self, request):
        data ={}
        try:
            self.user = request.user
            self.email = self.user.email
            self.avatar = self.user.avatar.url
            user = User.objects.get(pk = self.user.pk)
        except User.DoesNotExist:
            return Response({'error': "not found."}, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data['avatar'] == None:
                serializer.validated_data['avatar'] = self.avatar
    
            if self.email != serializer.validated_data.get('email'):
                self.user.is_active = False
                serializer.save()
                data = serializer.data
                current_site = get_current_site(request)
                mail_subject = "Email confirmation"
                message = render_to_string(
                    'email-temp.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }
                )
                to_email = serializer.validated_data.get('email')
                email = EmailMessage(
                    mail_subject,
                    message,
                    to=[to_email]
                )
                email.send()
                data['confirmation_email'] = "Confirmation mail sended to your mail."
                return Response(data, status=status.HTTP_200_OK)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)